from tensorflow.keras.models import load_model

model_file_path = 'Python/unfiltereModel.h5'
model = load_model(model_file_path)
loss, accuracy = model.evaluate(test_data, test_labels)