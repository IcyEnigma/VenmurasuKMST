import sacrebleu
from sacremoses import MosesDetokenizer
md = MosesDetokenizer(lang='en')
index = 22
while (index<=31):
# Open the test dataset human translation file and detokenize the references
  refs = []

  with open(f"/content/drive/MyDrive/Venmurasu Final/{index}eng_final.txt") as test:
      lines = test.readlines()
      l = [x[:-1] for x in lines if x!='\n']
      for line in l: 
          line = line.strip().split() 
          line = md.detokenize(line) 
          refs.append(line)
      
  print("Reference 1st sentence:", refs[0])

  # Open the translation file by the NMT model and detokenize the predictions
  preds = []

  with open(f"/content/drive/MyDrive/Venmurasu Final/GoogleEval/{index}translated.txt") as pred:  
      for line in pred: 
          line = line.strip().split() 
          line = md.detokenize(line) 
          preds.append(line)

  # Calculate BLEU for sentence by sentence and save the result to a file
  with open(f"/content/drive/MyDrive/Venmurasu Final/Google scores/{index}-GScore.txt", "w+") as output:
      scorelist = []
      for line in zip(refs,preds):
          test = line[0]
          pred = line[1]
          print(test, "\t--->\t", pred)
          output.write(str(test)+ "\t--->\t"+ str(pred)+"\n\n")
          bleu = sacrebleu.sentence_bleu(pred, [test], smooth_method='exp')
          print(bleu.score, "\n")
          scorelist.append(bleu.score)
          output.write(str(bleu.score) + "\n\n\n")
      avg = sum(scorelist)/len(scorelist)
      print(f"Average for file {index} : ", avg)
      output.write("Average : "+str(avg)+"\n")
  
  index+=1
