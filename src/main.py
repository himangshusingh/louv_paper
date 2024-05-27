import os
from flask import Flask, render_template, request, redirect, url_for
from louvain_algorithm import louvain
from visualize import visualize_communities
import datetime
import social as sc

app = Flask(__name__)

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Set the template folder path
template_folder = os.path.join(current_dir, 'templates')

# Initialize the Flask app with the template folder
app = Flask(__name__, template_folder=template_folder)


dataset = sc.les_miserables_graph()                        #dataset entry
"""
current available datasets:

1. karate_club_graph
2. davis_southern_women_graph
3. les_miserables_graphis the
4. florentine_families_graph
5. citation_network
"""

@app.route('/')
def index():
    """
    this is the home page of the application, loads the starting template
    """
    return render_template('view_communities.html')



@app.route('/detect_communities', methods=['GET', 'POST'])  
def detect_communities():
    """
    this is the function that detects communities in the dataset
    """
    if request.method == 'POST':
        dataset_name = request.form['dataset']                              #get the dataset name from the form
        if dataset_name == 'citation_network':
            return redirect(url_for('static', filename='citation/index.html'))
        dataset_functions = {
            'karate_club_graph': sc.karate_club_graph,
            'davis_southern_women_graph': sc.davis_southern_women_graph,
            'les_miserables_graph': sc.les_miserables_graph,
            'florentine_families_graph': sc.florentine_families_graph,
        }
        if dataset_name in dataset_functions:
            G = dataset_functions[dataset_name]()
            communities = louvain(G)                                        # calls the louvain() in louvain_algorithm.py

            # generate the timestamp
            current_datetime = datetime.datetime.now()
            timestamp = current_datetime.strftime("%d%m_%H%M")

            # generate the file with the timestamp
            output_file_name = f"graph_{dataset_name}_{timestamp}.html"
            output_file_path = os.path.join(current_dir, 'static','output', output_file_name)
            visualize_communities(G, communities, output_file=output_file_path)                 
            # Pass the generated file name to the template
            return render_template('detect_communities.html', output_file='output/' + output_file_name)         #calls the detect_communities.html to load the graph
        else:
            return render_template('error.html', message="Dataset not found"), 404 
    else:
        return render_template('view_communities.html')
    
if __name__ == '__main__':
    """
    specify the port number if needed if not then it defaults to 5000
    if default needed then just erase the port=8080
    """
    app.run()                                                           #port number / other specifications are in .flaskenv


# def start_command():
#     """Run the server."""
#     app.run(debug=True, port=8080)