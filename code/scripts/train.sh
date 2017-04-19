python /tensorflow/tensorflow/examples/image_retraining/retrain.py \
--bottleneck_dir=latteart_model/bottlenecks \
--how_many_training_steps 4000 \
--model_dir=latteart_model/inception \
--output_graph=latteart_model/retrained_graph.pb \
--output_labels=latteart_model/retrained_labels.txt \
--image_dir latteart_model/data
