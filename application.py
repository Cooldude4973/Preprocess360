from flask import Flask, render_template, request, redirect, url_for, send_file , jsonify
import pandas as pd
import matplotlib.pyplot as plt
import io
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder



app = Flask(__name__)
# file = None
# df_global = None
df = None


@app.route('/')
def home():
    # df = pd.read_csv(r'C:\Users\Sahil Chalke\Professional\Web development\Graph Maker\adult.csv')
    # table_html = df.to_html(classes='table table-striped', index=False)
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)

    if file:
    # Read the uploaded CSV file
        df = pd.read_csv(file)
        print(df.head())  # Debugging: Print the first few rows of the dataframe

    # Generate the plot (this is a basic example)
        plt.figure()
        df.plot(kind='line')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Plot from CSV Data')
        
        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
    
        return send_file(img, mimetype='image/png')
    
@app.route('/analyze', methods=['POST'])
def analyze_file():
    # global df_global
    global df
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file:
    # Read the uploaded CSV file
        df = pd.read_csv(file)
        headers = df.columns.to_list()
        return jsonify(headers)
    

@app.route('/nullcheck' , methods = ['POST'])
def check_null_values():
    # global df_global
    global df
    print(df.head())
    number_null_values = df.isna().sum().to_list()
    sum = 0
    for val in number_null_values:
        sum += val

    return jsonify(val)

@app.route('/unique' , methods = ['POST'])
def unique_values():
    global df
    # if 'file' not in request.files:
    #     return redirect(request.url)
    
    # file = request.files['file']
    # df = pd.read_csv(file)
    headers = df.columns.to_list()
    listUnique = []
    for head in headers:

        listUnique.append(df[head].unique().tolist())
    return jsonify({'headers': headers, 'unique': listUnique})


@app.route('/removeduplicates' , methods = ['POST'])
def removeDuplicates():
    global df
    # if 'file' not in request.files:
    #     return redirect(request.url)
    # file = request.files['file']
    # df = pd.read_csv(file)
    # print("THESE ARE THE NUMBER OF DUPLICATES IN THE DATASET")
    # print("hELLO WORLD " , df.duplicated().sum())
    duplicate_count = int(df.duplicated().sum())
    df.drop_duplicates(inplace=True)
    return jsonify({'duplicate_count': duplicate_count})




@app.route('/missing' , methods = ['POST'])
def findMissing():
    print("Hello World")
    if 'file' not in request.files:
        return redirect(request.url)
    mval = request.form.get('mval')
    file = request.files['file']    
    df = pd.read_csv(file)
    print(df.head())
    print(mval)
    print(df.isin([mval]).sum())
    nullList = df.isin([mval]).sum()
    sum = 0
    for val in nullList:
        sum += val
    # print(mval.dtypes)  
    print(sum)
    return jsonify(sum)

@app.route('/removemissing' , methods = ['POST'])
def removemissing():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    selectedColumns = request.form.get('selectedColumns')
    mval = request.form.get('missingVal')
    # print(selectedColumns)
    df = pd.read_csv(file)
    for head in selectedColumns:
        df = df[df[head] != mval]


@app.route('/download' , methods = ['GET'])
def download_file():
    print('downloading...')
    global df
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    # Send the CSV file to the user
    return send_file(
        io.BytesIO(csv_buffer.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='data.csv'
    )
@app.route('/replaceMissing' , methods = ['POST'])
def replaceMissing():
    global df
    mval = request.form.get('mval')
    strategy = request.form.get('strategy')
    selectedColumns = request.form.get('selectedColumns')
    imputer = SimpleImputer(strategy=strategy, missing_values=mval)
    for column in selectedColumns:
        df[column] = imputer.fit_transform(df[[column]]).ravel()



# HANDLING CATEGORICAL DATA 
@app.route('/labelEncode' , methods = ['POST'])
def labelEncode():
    global df
    selectedColumns = request.form.get('selectedColumns')

    lbl_encoder=LabelEncoder()
    for column in selectedColumns:
        df[column]=lbl_encoder.fit_transform(df[column])

@app.route('/onehotEncode' , methods = ['POST'])
def onehotEncode():
    global df
    selectedColumns = request.form.get('selectedColumns')

    onehotEncoder = OneHotEncoder()
    for column in selectedColumns:
        df[column]=onehotEncoder.fit_transform(df[column])


@app.route('/info' , methods = ['GET'])
def info():
    # global df
    df = pd.read_csv(r'C:\Users\Sahil Chalke\Professional\Web development\Graph Maker\adult.csv')
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    return  jsonify({"info" :info_str})


@app.route('/replace' , methods = ['POST'])
def replace():
    global df
    column = request.form.get('column')
    toreplace = request.form.get('toreplace')
    replacewith = request.form.get('replacewith')
    df[column]=df[column].replace(toreplace,replacewith)



@app.route('/describe' , methods = ['POST'])
def describe():
    global df
    describe = df.describe()
    return jsonify({"decribe" : describe})


@app.route('/displayHead' , methods = ['POST'])
def displayHead():
    global df
    head = df.head()
    # df_dict = df.to_dict(orient='records')
    
    # Return the DataFrame as JSON
    rendered_html = head.to_html(classes='data', header="true")
    sanitized_html = rendered_html.replace('\n', '').replace('\r', '').replace('  ', '').replace('[\'',' ').replace('\']' , ' ')
    return render_template('index.html', tables=[sanitized_html])






if __name__ == '__main__':
    app.run(debug=True)
