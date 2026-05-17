This directory contains all the files of our final project.

acne_split is the dataset we used for the RandomForest Classifier for detection of acne level. 

images.v1i.multiclass is the dataset we used for the SVM model for the detection of other various skin conditions (acne, dark circles, dark spots, dry skin, normal skin, oily skin, pores, wrinkles) 

skinTone is the dataset we used for our CNN that classified skin tones (Fair, Medium, Dark).

acne_classification_rf.py is the python file that creates and evaluates our RandomForest model to detect various levels of acne.
In the python file, it saves rf_model.pkl that is used in the streamlit to evaluate a person's acne level. 

multilabel_svm.py is the python file that creates and evaluates our SVM model to detect other various skin conditions.
It detects also acne (though not at the accuracy the RandomForest model does), dark circles, dark spots, dry skin, normal skin, oily skin, pores, and wrinkles.
In the python file, it saves svm_multilabel.pkl that is used in the streamlit to evaluate a person's skin conditions. 

skin_tone_classification_cnn.py is the python file that creates and evaluates our CNN model to detect skin tone.
In the python file, it saves skin_tone_model.h5 that is used in the streamlit to evaluate a person's skin conditions. 

app.py is our streamlit that you can run to see an interface where you an input a picture (pictures given in test_images_streamlit). 
You need to run using streamlit run app.py

We have our rf_model.pkl but unfortunately could upload our svm_multilabel.pkl and skin_tone_model.h5. To successfully run our app.py, you need to run multilabel_svm.py to get svm_multilabel.pkl and run skin_tone_classification_cnn.py to get skin_tone_model.h5. Once that is saved into the current directory, the app.py should load all those models are run. 

You can also rerun acne_classification_rf.py to produce and new rf_model.pkl and use that saved model when running the streamlit.

test_images_streamlit have some images you can input into the streamlit to see how it works!

model_results have the quantitative results from each model including the classification report of each model, the F1 scores of each model, and the confusion matricies of each model. 
