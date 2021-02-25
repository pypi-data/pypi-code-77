from typing import Dict
from attrdict import AttrDict

import torch

from transformers import (
    AutoModel,
    AutoModelForPreTraining,
    AutoModelForCausalLM,
    AutoModelForMaskedLM,
    AutoModelForSeq2SeqLM,
    AutoModelForSequenceClassification,
    AutoModelForMultipleChoice,
    AutoModelForNextSentencePrediction,
    AutoModelForTokenClassification,
    AutoModelForQuestionAnswering,
    AutoConfig,
    AutoTokenizer,
)
from transformers.optimization import AdamW, Adafactor, get_scheduler
from datasets import load_dataset

from determined.pytorch import (
    LRScheduler,
    PyTorchTrial,
    PyTorchTrialContext,
)

from ._arg_parser import (
    default_parse_config_tokenizer_model_args,
    default_parse_optimizer_lr_scheduler_args,
    parse_dict_to_dataclasses,
    OptimizerKwargs,
    LRSchedulerKwargs,
    DatasetKwargs,
)


MODEL_MODES = {
    "base": AutoModel,
    "pretraining": AutoModelForPreTraining,
    "causal-lm": AutoModelForCausalLM,
    "masked-lm": AutoModelForMaskedLM,
    "seq2seq-lm": AutoModelForSeq2SeqLM,
    "sequence-classification": AutoModelForSequenceClassification,
    "multiple-choice": AutoModelForMultipleChoice,
    "next-sentence": AutoModelForNextSentencePrediction,
    "token-classification": AutoModelForTokenClassification,
    "question-answering": AutoModelForQuestionAnswering,
}


def build_using_auto(
    config_args: [Dict, AttrDict],
    tokenizer_args: [Dict, AttrDict],
    model_mode: str,
    model_args: [Dict, AttrDict],
):
    """
    Build the config, tokenizer, and model using tranformer's
    Auto classes.

    Args:
        config_args: arguments for transformers configuration classes
        tokenizer_args: arguments for transformers tokenizer classes
        model_mode: one of the tasks supported by transformers, see MODEL_MODES for
            the supported options
        model_args: arguments for transformers model classes

    Returns:
        transformer config, tokenizer, and model
    """
    config = AutoConfig.from_pretrained(**config_args)
    tokenizer = AutoTokenizer.from_pretrained(**tokenizer_args)
    model_mode = MODEL_MODES[model_mode]
    model_args["config"] = config
    model = model_mode.from_pretrained(**model_args)
    return config, tokenizer, model


def group_parameters_for_optimizer(
    model: torch.nn.Module, weight_decay: float, no_decay=("bias", "LayerNorm.weight")
):
    """
    Group parameters by whether weight_decay is applied or not.

    Args:
        model: model supplying the learnable parameters
        weight_decay: value for weight_decay
        no_decay: variable names that should not have weight_decay applied
    Returns:
        grouped parameters according to whether weight_decay should be applied
    """
    return [
        {
            "params": [
                p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)
            ],
            "weight_decay": weight_decay,
        },
        {
            "params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
            "weight_decay": 0.0,
        },
    ]


def build_default_optimizer(
    model: torch.nn.Module, optimizer_args: OptimizerKwargs
) -> torch.optim.Optimizer:
    """
    This follows the function in transformer's Trainer to construct the optimizer.

    Args:
        model: model whose parameters will be updated by the optimizer
        weight_decay: weight_decay factor to apply to weights
        optimizer_args: see OptimizerKwargs in _arg_parser.py for expected fields
    Returns:
        optimizer configured accordingly
    """
    optimizer_grouped_parameters = group_parameters_for_optimizer(
        model, optimizer_args.weight_decay
    )
    if optimizer_args.adafactor:
        return Adafactor(
            optimizer_grouped_parameters,
            lr=optimizer_args.learning_rate,
            scale_parameter=optimizer_args.scale_parameter,
            relative_step=optimizer_args.relative_step,
        )
    return AdamW(
        optimizer_grouped_parameters,
        lr=optimizer_args.learning_rate,
        betas=(optimizer_args.adam_beta1, optimizer_args.adam_beta2),
        eps=optimizer_args.adam_epsilon,
    )


def build_default_lr_scheduler(
    optimizer: torch.optim.Optimizer,
    scheduler_args: LRSchedulerKwargs,
):
    """
    This follows the function in transformer's Trainer to construct the lr_scheduler.

    Args:
        optimizer: optimizer to apply lr_scheduler to
        scheduler_args: see LRSchedulerKwargs in _arg_parser.py for expected fields.
    Returns:
        lr_scheduler configured accordingly
    """
    return get_scheduler(
        scheduler_args.lr_scheduler_type,
        optimizer,
        num_warmup_steps=scheduler_args.num_warmup_steps,
        num_training_steps=scheduler_args.num_training_steps,
    )


def default_load_dataset(data_config: [Dict, AttrDict]):
    """
    Creates the dataset using HuggingFace datasets' load_dataset method.
    If a dataset_name is provided, we will use that long with the dataset_config_name.
    Otherwise, we will create the dataset using provided train_file and validation_file.

    Args:
        data_config: arguments for load_dataset.  See DatasetKwargs for expected fields.
    Returns:
        Dataset returned from datasets.load_dataset.
    """
    (data_config,) = parse_dict_to_dataclasses((DatasetKwargs,), data_config)
    # This method is common in nearly all main HF examples.
    if data_config.dataset_name is not None:
        # Downloading and loading a dataset from the hub.
        datasets = load_dataset(data_config.dataset_name, data_config.dataset_config_name)
        if "validation" not in datasets.keys():
            assert (
                "validation_split_percentage" in data_config
            ), "Validation split not provided by this huggingface dataset. Please specify validation_split_percentage in data_config for use to create validation set"
            datasets["validation"] = load_dataset(
                data_config.dataset_name,
                data_config.dataset_config_name,
                split=f"train[:{data_config.validation_split_percentage}%]",
            )
            datasets["train"] = load_dataset(
                data_config.dataset_name,
                data_config.dataset_config_name,
                split=f"train[{data_config.validation_split_percentage}%:]",
            )
    else:
        data_files = {}
        if data_config.train_file is not None:
            data_files["train"] = data_config.train_file
        if data_config["validation_file"] is not None:
            data_files["validation"] = data_config.validation_file
        extension = data_config.train_file.split(".")[-1]
        if extension == "txt":
            extension = "text"
        datasets = load_dataset(extension, data_files=data_files)
    return datasets


class BaseTransformerTrial(PyTorchTrial):
    """
    This is the base trial class for transformers with a default init and train_batch method.

    You can subclass BaseTransformerTrial to customize a trial for your own usage by filing in
    the expected methods for data loading and evaluation.

    See examples/huggingface/token-classification/ner_trial.py for an example.
    """

    def __init__(self, context: PyTorchTrialContext) -> None:
        self.context = context
        self.hparams = AttrDict(context.get_hparams())
        self.data_config = AttrDict(context.get_data_config())

        # Parse hparams and data_config.
        config_args, tokenizer_args, model_args = default_parse_config_tokenizer_model_args(
            self.hparams
        )
        optimizer_args, scheduler_args = default_parse_optimizer_lr_scheduler_args(self.hparams)

        self.config, self.tokenizer, self.model = build_using_auto(
            config_args, tokenizer_args, self.hparams.model_mode, model_args
        )
        self.model = self.context.wrap_model(self.model)

        self.optimizer = self.context.wrap_optimizer(
            build_default_optimizer(self.model, optimizer_args)
        )

        if self.hparams.use_apex_amp:
            self.model, self.optimizer = self.context.configure_apex_amp(
                models=self.model,
                optimizers=self.optimizer,
            )

        self.lr_scheduler = self.context.wrap_lr_scheduler(
            build_default_lr_scheduler(self.optimizer, scheduler_args),
            LRScheduler.StepMode.STEP_EVERY_BATCH,
        )
        self.grad_clip_fn = (
            lambda x: torch.nn.utils.clip_grad_norm_(x, optimizer_args.max_grad_norm)
            if optimizer_args.max_grad_norm > 0
            else None
        )

    def train_batch(self, batch, epoch_idx: int, batch_idx: int):
        # See https://github.com/huggingface/transformers/blob/61abd50b98de4cd8f6024d77154a0326d16f1db5/src/transformers/trainer.py#L1114
        # By default, all models return the loss in the first element.
        outputs = self.model(**batch)
        loss = outputs[0]
        self.context.backward(loss)
        self.context.step_optimizer(self.optimizer, self.grad_clip_fn)
        return loss
