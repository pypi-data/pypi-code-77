from sentence_transformers import SentenceTransformer, SentencesDataset, models
from sentence_transformers.evaluation import SentenceEvaluator, SequentialEvaluator, InformationRetrievalEvaluator
from sentence_transformers.readers import InputExample
from transformers import AdamW
from torch import nn
from torch.utils.data import DataLoader
from torch.optim import Optimizer
from tqdm.autonotebook import trange
from typing import Dict, Type, List, Callable, Iterable, Tuple
import logging
import time
import random

logger = logging.getLogger(__name__)

class TrainRetriever:
    
    def __init__(self, model_name: str, batch_size: int = 64, max_seq_length: int = 350):
        self.model_name = model_name
        self.batch_size = batch_size
        self.max_seq_length = max_seq_length

        word_embedding_model = models.Transformer(model_name, max_seq_length=self.max_seq_length)
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
        self.model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    
    def load_train(self, corpus: Dict[str, Dict[str, str]], queries: Dict[str, str], 
                   qrels: Dict[str, Dict[str, int]]) -> List[Type[InputExample]]:
        
        query_ids = list(queries.keys())
        train_samples = []

        for idx, start_idx in enumerate(trange(0, len(query_ids), self.batch_size, desc='Adding Input Examples')):
            query_ids_batch = query_ids[start_idx:start_idx+self.batch_size]
            for query_id in query_ids_batch:
                for corpus_id, score in qrels[query_id].items():
                    if score >= 1: # if score = 0, we don't consider for training
                        s1 = queries[query_id]
                        s2 = corpus[corpus_id]
                        train_samples.append(InputExample(guid=idx, texts=[s1, s2], label=1))

        logger.info("Loaded {} training pairs.".format(len(train_samples)))
        return train_samples
    
    def prepare_train(self, train_samples: List[Type[InputExample]], shuffle: bool = True) -> DataLoader:
        
        train_data = SentencesDataset(train_samples, model=self.model)
        train_dataloader = DataLoader(train_data, shuffle=shuffle, batch_size=self.batch_size)
        return train_dataloader
    
    def load_ir_evaluator(self, corpus: Dict[str, Dict[str, str]], queries: Dict[str, str], 
                 qrels: Dict[str, Dict[str, int]], max_corpus_size: int = None, name: str = "eval") -> SentenceEvaluator:

        if len(queries) <= 0:
            raise ValueError("Dev Set Empty!, Cannot evaluate on Dev set.")
        
        rel_docs = {}
        corpus_ids = set()
        
        # need to convert corpus to cid => doc      
        corpus = {idx: corpus[idx].get("text") + " " + corpus[idx].get("title") for idx in corpus}
        
        # need to convert dev_qrels to qid => Set[cid]        
        for query_id, metadata in qrels.items():
            rel_docs[query_id] = set()
            for corpus_id, score in metadata.items():
                if score >= 1:
                    corpus_ids.add(corpus_id)
                    rel_docs[query_id].add(corpus_id)
        
        if max_corpus_size:
            # check if length of corpus_ids > max_corpus_size
            if len(corpus_ids) > max_corpus_size:
                raise ValueError("Your maximum corpus size should atleast contain {} corpus ids".format(len(corpus_ids)))
            
            # Add mandatory corpus documents
            new_corpus = {idx: corpus[idx] for idx in corpus_ids}
            
            # Remove mandatory corpus documents from original corpus
            for corpus_id in corpus_ids:
                corpus.pop(corpus_id, None)
            
            # Sample randomly remaining corpus documents
            for corpus_id in random.sample(list(corpus), max_corpus_size - len(corpus_ids)):
                new_corpus[corpus_id] = corpus[corpus_id]

            corpus = new_corpus

        logger.info("{} set contains {} documents and {} queries".format(name, len(corpus), len(queries)))
        return InformationRetrievalEvaluator(queries, corpus, rel_docs, name=name)
    
    def load_dummy_evaluator(self) -> SentenceEvaluator:
            return SequentialEvaluator([], main_score_function=lambda x: time.time())

    def fit(self, 
            train_objectives: Iterable[Tuple[DataLoader, nn.Module]],
            evaluator: SentenceEvaluator = None,
            epochs: int = 1,
            steps_per_epoch = None,
            scheduler: str = 'WarmupLinear',
            warmup_steps: int = 10000,
            optimizer_class: Type[Optimizer] = AdamW,
            optimizer_params : Dict[str, object]= {'lr': 2e-5, 'eps': 1e-6, 'correct_bias': False},
            weight_decay: float = 0.01,
            evaluation_steps: int = 0,
            output_path: str = None,
            save_best_model: bool = True,
            max_grad_norm: float = 1,
            use_amp: bool = False,
            callback: Callable[[float, int, int], None] = None
            ):
        
        # Train the model
        logger.info("Starting to Train...")

        self.model.fit(train_objectives=train_objectives,
                evaluator=evaluator,
                epochs=epochs,
                steps_per_epoch=steps_per_epoch,
                warmup_steps=warmup_steps,
                optimizer_class=optimizer_class,
                scheduler=scheduler,
                optimizer_params=optimizer_params,
                weight_decay=weight_decay,
                output_path=output_path,
                evaluation_steps=evaluation_steps,
                save_best_model=save_best_model,
                max_grad_norm=max_grad_norm,
                use_amp=use_amp,
                callback=callback)