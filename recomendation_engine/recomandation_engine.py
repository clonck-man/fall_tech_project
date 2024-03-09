import pandas as pd


class recommandation_engine:
    def __init__(self):
        pass

    def predict(self):
        pass

    def predict_selection(self, selection_size=10):
        pass


class random_engin(recommandation_engine):

    def __init__(self, datas: pd.DataFrame):
        super().__init__()
        self.datas = datas

    def predict(self):
        return self.datas.sample(n=1)

    def predict_selection(self, selection_size=10):
        return self.datas.sample(n=selection_size)
