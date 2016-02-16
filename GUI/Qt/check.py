class Check:
    @staticmethod
    def check():
        try:
            import PyQt4
            return True
        except:
            return False