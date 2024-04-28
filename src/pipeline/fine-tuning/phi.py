


if __name__ == "__main__":
    # Use a pipeline as a high-level helper
    from transformers import pipeline

    pipe = pipeline("text-generation", model="microsoft/Phi-3-mini-128k-instruct", trust_remote_code=True)
    # Load model directly
    from transformers import AutoTokenizer, AutoModelForCausalLM

    tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct", trust_remote_code=True)


    from datasets import load_dataset

    dataset = load_dataset['yelp_review_full']
    print(dataset[:10])

    from transformers import AutoTokenizer

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)


    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
    small_eval_dataset = tokenized_datasets["test"].shuffle(seed=42).select(range(1000))

    from transformers import TrainingArguments

    training_args = TrainingArguments(output_dir="test_trainer")

    import numpy as np
    import evaluate

    metric = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)

    from transformers import TrainingArguments, Trainer

    training_args = TrainingArguments(output_dir="test_trainer", eval_strategy="epoch")

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        compute_metrics=compute_metrics,
    )

    #trainer.train()