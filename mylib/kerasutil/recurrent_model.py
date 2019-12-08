from .base_model import *

@dataclass()
class RNNContext(BaseContext):
    window_size = 14


class RNNWrapper(BaseModel):

    def __init__(self, context: RNNContext):
        super().__init__(context)

    def preprocess(self, data):
        from sklearn.preprocessing import MinMaxScaler
        mms = MinMaxScaler()
        mms.fit(data)
        minmax = mms.transform(data)
        return minmax

    def make_data_and_label(self, data):
        inp, out = [], []
        for i in range(len(data) - self.context.window_size):
            inp.append(data[i:i+self.context.window_size])
            out.append(data[i + self.context.window_size])
        X = np.array(inp).reshape(len(inp), self.context.window_size, data.shape[1])
        y = np.array(out).reshape(len(out), data.shape[1])
        return X, y

    def create_basic_lstm_model(self, X, unit_size=64):
        from keras.layers import LSTM, Dense
        shape = np.shape(X)
        input_layer = keras.Input(shape=(self.context.window_size, shape[2]))
        lstm_layer = LSTM(unit_size, return_sequences=False)(input_layer)
        predictions = Dense(shape[2])(lstm_layer)
        model = keras.models.Model(input=input_layer, output=predictions)
        model.compile(loss=self.context.loss,
                      optimizer=self.context.optimizer,
                      metrics=self.context.metrics)
        return model

    def fit(self, model:keras.models.Model, X, y):
        tensor_board = keras.callbacks.TensorBoard(log_dir=self.context.tensor_board_dir, histogram_freq=1)
        early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', mode='auto', patience=20)
        model.fit(X, y,
                  batch_size=self.context.batch_size,
                  epochs=self.context.epochs,
                  validation_split=self.context.validation_split,
                  callbacks=[tensor_board, early_stopping]
                  )
        return model

    def rmse_score(self, model: keras.models.Model, Xtrain, Xtest, ytrain, ytest, index=0):
        """
        root mean squared error
        """
        pred_train, pred_test = model.predict(Xtrain), model.predict(Xtest)
        pred_list_train = np.array([pred_train[:, index]])
        pred_list_test = np.array([pred_test[:, index]])
        from sklearn.metrics import mean_squared_error
        rmse_train = [np.sqrt(mean_squared_error(ytrain[:, index], _y)) for _y in pred_list_train]
        rmse_test = [np.sqrt(mean_squared_error(ytest[:, index], _y)) for _y in pred_list_test]
        return rmse_train, rmse_test

    def high_low_score(self, answer, prediction, index=0):
        highlow = lambda l, c: 1 if c > l else -1 if c < l else 0
        match = 0
        for i, v in enumerate(answer[1:]):
            li = i - 1
            la, ca = answer[li, index], v[index]
            lp, cp = prediction[li, index], prediction[i-1, index]
            ans = highlow(la, ca)
            pred = highlow(lp, cp)
            if ans == pred:
                match += 1
        return match

    def high_low_probability_score(self,answer, prediction, index=0):
        highlow = lambda x: 1 if x > 0.5 else -1 if x < 0.5 else 0
        match = 0
        for i, v in enumerate(answer[1:]):
            ans = highlow(answer[i, index])
            pred = highlow(prediction[i, index])
            if ans == pred:
                match += 1
        return match

    def high_low_probavility_score_with_border(self, answer, prediction, index=0, high=0.7, low=0.3):
        highlow = lambda x: 1 if x > high else -1 if x < low else 0
        match, total = 0, 0
        for i, v in enumerate(answer[1:]):
            ans = highlow(answer[i, index])
            pred = highlow(prediction[i, index])
            if pred == 0:
                continue
            if ans == pred:
                match += 1
            total += 1
        return match, total