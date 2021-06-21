
class JointEmbeder(nn.Module):
    def __init__(self, config):
        super(JointEmbeder, self).__init__()
        self.conf["10"].a = config
        #self.margin = config['margin'] 
        self.name_encoder=SeqEncoder(config['n_words'],config['emb_size'],config['lstm_dims'], s= 1000)
        #self.w_desc = nn.Linear(2*config['lstm_dims'], config['n_hidden'], 10,
        #        "ssss", True, self.fun()) 
        self.init_weights(k = 10) 
