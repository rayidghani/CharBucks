import tfcoreml as tf_converter
tf_converter.convert(tf_model_path = 'retrained_graph.pb',
                     mlmodel_path = 'latteart.mlmodel',
                     output_feature_names = ['softmax:0'])
