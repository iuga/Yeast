class Step():
    """
    Yeast Step Definition:
    All Steps must inherit from this class.

    Workflow:
    init() -->
               prepare() --> do_prepare() -->
                                             bake() -->                                  do_bake()
                                                        validate() --> do_validate() -->

    Notes:
    It contains some methods that should be redefined by childs if neccesary like:
    - do_prepare() is called by prepare()
    - do_bake() is called by bake()
    - do_validate() is called by validate()
    """
    def prepare(self, df):
        """
        During this phase the original df must not be transformed.

        :returns self for chaining
        """
        self.do_prepare(df)
        return self

    def bake(self, df):
        """
        Execute the recipe transforming the dataframe and return it but before, validate it.

        :returns the transformed dataframe
        """
        self.validate(df)
        return self.do_bake(df)

    def validate(self, df):
        """
        Validate the step including parameters and further errors
        The return will be ignored
        """
        return self.do_validate(df)

    def do_prepare(self, df):
        """
        Let subclasses override this operation
        """
        return self

    def do_bake(self, df):
        """
        Let subclasses override this operation
        """
        return df

    def do_validate(self, df):
        """
        Let subclasses override this operation
        """
        return self
