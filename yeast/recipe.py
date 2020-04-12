class Pipeline():

    def prepare(self, df):
        return self

    def bake(self, df):
        return self

    def prepare_bake(self, df):
        return self.prepare(df).transform(df)
