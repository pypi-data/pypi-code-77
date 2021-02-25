import logging
import os
from datetime import datetime
from os import path
from logging.config import fileConfig
import numpy as np
import wandb
from sklearn.metrics import precision_recall_fscore_support
from torch import nn
from transformers import AutoTokenizer, AutoModel
import torch

fileConfig(path.join(path.dirname(__file__), '../resources/log_config.ini'))
logger = logging.getLogger('camembert-ner-ft')


def count_parameters(mdl):
    return sum(p.numel() for p in mdl.parameters() if p.requires_grad)


def init_tokenizer(model_name):
    logger.info("🍌 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    return tokenizer


def mask_tokens(inputs, tokenizer):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    inputs = inputs.to(device)
    labels = inputs.clone().to(device)
    probability_matrix = torch.full(labels.shape, 0.15).to(device)
    masked_indices = torch.bernoulli(probability_matrix).bool().to(device)
    labels[~masked_indices] = -100  # We only compute loss on masked tokens

    # 80% of the time, we replace masked input tokens with tokenizer.mask_token ([MASK])
    indices_replaced = torch.bernoulli(torch.full(labels.shape, 0.8)).bool().to(device) \
                       & masked_indices
    inputs[indices_replaced] = tokenizer.get_vocab()['<mask>']

    # 10% of the time, we replace masked input tokens with random word
    indices_random = (torch.bernoulli(torch.full(labels.shape, 0.1)).bool().to(device)
                      & masked_indices & ~indices_replaced).to(device)
    random_words = torch.randint(len(tokenizer.get_vocab()) - 1,
                                 labels.shape, dtype=torch.long).to(device)
    inputs[indices_random] = random_words[indices_random]

    # The rest of the time (10% of the time) we keep the masked input tokens unchanged
    return inputs.tolist(), labels.tolist()


def save_model(classifier, hyperparameter_defaults, id_fold, model, model_name):
    logger.info("💾 saving model ..")
    current_datetime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    save_location = hyperparameter_defaults['model_path']
    model_name = f'{model_name}-' \
                 f'{current_datetime}-fold-{id_fold + 1}.bin'
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    save_location = os.path.join(save_location, model_name)
    torch.save({model, classifier}, save_location)
    wandb.save(save_location)


def monitor_output_example(batch, dataloader, labels, predictions_scores):
    decode_ids = dataloader.dataset.tokenizer.convert_ids_to_tokens(batch['tokens'][-1])
    seq_token_index = decode_ids.index('</s>')
    decode_ids = decode_ids[1:seq_token_index]
    true_labels = [labels[label_id] for label_id in batch['target'][-1][1:seq_token_index]]
    pred_labels = [labels[label_id]
                   for label_id in predictions_scores[-1].argmax(dim=1)[1:seq_token_index]]
    logger.info('here is one example tagged by the model (text/true labels/pred labels):')
    logger.info(decode_ids)
    logger.info(true_labels)
    logger.info(pred_labels)


def init_model(model_name, device):
    logger.info("🍌 Loading model...")
    model = AutoModel.from_pretrained(model_name)
    if device == 'cuda':
        model = nn.DataParallel(model).to(device)
    model = model.to(device)
    logger.info(f'The model has {count_parameters(model):,} trainable parameters')
    return model


def monitor_model_eval(predictions_scores: torch.Tensor,
                       batch: dict) -> (np.float, np.float, np.float):
    y_true = batch['target'].contiguous().reshape(-1)
    y_pred = predictions_scores.contiguous().argmax(dim=2).reshape(-1)
    pad_idx = (y_true == -100).nonzero(as_tuple=False).flatten()
    y_pred[pad_idx] = -100
    labels = np.intersect1d(y_pred.unique(), y_true.unique())
    labels = np.delete(labels, np.where(labels == -100))
    precision, recall, f1_score, _ = precision_recall_fscore_support(y_true,
                                                                     y_pred,
                                                                     average='macro',
                                                                     labels=labels)
    return precision, recall, f1_score
