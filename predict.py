import tensorflow as tf
import tokenization
import numpy as np

saved_model_path = "./saved_model/1"
label_dict = {0: "negative", 1: "positive"}

loaded = tf.saved_model.load(saved_model_path)
predict_fn = loaded.signatures["serving_default"]


class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self,
                 input_ids,
                 input_mask,
                 segment_ids,
                 label_id,
                 is_real_example=True):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_id = label_id
        self.is_real_example = is_real_example


class Predictor(object):
    def __init__(self):
        self.max_seq_len = 128
        self.tokenizer = tokenization.FullTokenizer(vocab_file="./albert_tiny/vocab.txt", do_lower_case=False)

    def predict(self, text_list: list):
        if len(text_list) == 0:
            return None
        features = self.convert_to_feature(text_list)
        input_feat = {"input_word_ids": tf.constant([feature.input_ids for feature in features]),
                      "input_mask": tf.constant([feature.input_mask for feature in features]),
                      "input_type_ids": tf.constant([feature.segment_ids for feature in features]), }
        output = predict_fn(**input_feat)

        return [label_dict[val] for val in np.argmax(output["pred"], axis=1)]

    def convert_to_feature(self, sentences: list):
        features = []
        for sentence in sentences:
            tokens = str(sentence)

            if len(tokens) >= self.max_seq_len - 1:
                tokens = tokens[0:(self.max_seq_len - 2)]
            ntokens = []
            segment_ids = []
            label_ids = [0]
            ntokens.append("[CLS]")
            segment_ids.append(0)

            for i, token in enumerate(tokens):
                ntokens.append(token)
                segment_ids.append(0)

            ntokens.append("[SEP]")
            segment_ids.append(0)

            input_ids = self.tokenizer.convert_tokens_to_ids(ntokens)
            input_mask = [1] * len(input_ids)

            while len(input_ids) < self.max_seq_len:
                input_ids.append(0)
                input_mask.append(0)
                segment_ids.append(0)
                ntokens.append("**NULL**")

            assert len(input_ids) == self.max_seq_len
            assert len(input_mask) == self.max_seq_len
            assert len(segment_ids) == self.max_seq_len

            feature = InputFeatures(
                input_ids=input_ids,
                input_mask=input_mask,
                segment_ids=segment_ids,
                label_id=label_ids,
            )
            features.append(feature)

        return features
