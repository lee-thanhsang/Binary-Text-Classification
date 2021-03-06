import numpy as np


class MultinomialNaiveBayes():

    def __init__(self):
        self.trained = False
        self.likelihood = 0
        self.prior = 0
        self.smooth = True
        self.smooth_param = 1
        
    def get_scores(self,x,w):
        '''
        Computes the dot product between X,w
        '''
        return np.dot(x,w)

    def train(self, x, y):
        # n_docs = no. of documents
        # n_words = no. of unique words    
        n_docs, n_words = x.shape
#        print "printing n_docs"
#        print n_docs
#        print "printing n_words"
#        print n_words
        
        # classes = a list of possible classes
        classes = np.unique(y)
#        print "printing classes"
#        print classes
#        
        # n_classes = no. of classes
        n_classes = np.unique(y).shape[0]
#        print "printing n_classes"
#        print n_classes
        
        # initialization of the prior and likelihood variables
        prior = np.zeros(n_classes)
#        print "printing prior structure"
#        print prior.shape
        
        likelihood = np.zeros((n_words,n_classes))
#        print "printing likelihood structure"
#        print likelihood.shape
        
        # TODO: This is where you have to write your code!
        # You need to compute the values of the prior and likelihood parameters
        # and place them in the variables called "prior" and "likelihood".
        # Examples:
            # prior[0] is the prior probability of a document being of class 0
            # likelihood[4, 0] is the likelihood of the fifth(*) feature being 
            # active, given that the document is of class 0
            # (*) recall that Python starts indices at 0, so an index of 4 
            # corresponds to the fifth feature!      
        # You need to incorporate self.smooth_param in likelihood calculation  
        ###########################
        no_doc_class = np.zeros(n_classes) #no of documents per class
        word_doc_class0 = np.zeros(n_words) #no of words for class o
        word_doc_class1 = np.zeros(n_words) #no of words for class 1
        word_doc_class2 = np.zeros(n_words) #no of words for class 2
        for i in range(n_docs):
            if y[i][0] == 0: #check if document belongs to class 0
                no_doc_class[0] +=1 #increase the counter of class 0
                for j in range(n_words): 
                    word_doc_class0[j]+=x[i][j] #creates a arrray of all words in class 0
            elif y[i][0]==1:  #check if document belongs to class 1
                no_doc_class[1] +=1 #increase the counter of class 1
                for j in range(n_words):
                    word_doc_class1[j]+=x[i][j]    #creates a arrray of all words in class 1
            else:  #check if document belongs to class 1
                no_doc_class[2] +=1 #increase the counter of class 1
                for j in range(n_words):
                    word_doc_class2[j]+=x[i][j]    #creates a arrray of all words in class 1
                    
   
         #prior is
        prior[0] = 1.0 * no_doc_class[0]/ n_docs
        prior[1] = 1.0 * no_doc_class[1]/ n_docs
        #prior[2] = 1.0 * no_doc_class[2]/ n_docs        
        #likelihood
        for i in range(n_words):
            likelihood[i][0]= (word_doc_class0[i]+self.smooth_param)/(word_doc_class0.sum()+self.smooth_param*n_words)
            likelihood[i][1]= (word_doc_class1[i]+self.smooth_param)/(word_doc_class1.sum()+self.smooth_param*n_words)
            #likelihood[i][2]= (word_doc_class2[i]+self.smooth_param)/(word_doc_class2.sum()+self.smooth_param*n_words)        

        ###########################

        params = np.zeros((n_words+1,n_classes))
        for i in range(n_classes): 
            # log probabilities
            params[0,i] = np.log(prior[i])
            with np.errstate(divide='ignore'): # ignore warnings
                params[1:,i] = np.nan_to_num(np.log(likelihood[:,i]))
        self.likelihood = likelihood
        self.prior = prior
        self.trained = True
        return params
    
    def get_label(self,x,w):
        '''
        Computes the label for each data point
        '''
        scores = np.dot(x,w)
        return np.argmax(scores,axis=1).transpose()

    def test(self,x,w):
        '''
        Classifies the points based on a weight vector.
        '''
        if self.trained == False:
            raise ValueError("Model not trained. Cannot test")
            return 0
        x = self.add_intercept_term(x)
        return self.get_label(x,w)

    def add_intercept_term(self,x):
        ''' Adds a column of ones to estimate the intercept term for separation boundary'''
        nr_x, nr_f = x.shape
        intercept = np.ones([nr_x,1])
        x = np.hstack((intercept,x))
        return x

    def evaluate(self,truth,predicted):
        correct = 0.0
        total = 0.0
        for i in range(len(truth)):
            if(truth[i] == predicted[i]):
                correct += 1
            total += 1
        return 1.0*correct/total
    