from django.shortcuts import render, get_object_or_404, get_list_or_404

from.models import DecisionTreeNode, DecisionTreeChoice, DecisionTreePath

def decision_tree_view(request):
    #make sure only one root node present!
    root_node = get_object_or_404(DecisionTreeNode, node_type = 'root')
    nodes = []
    paths_taken = []
    paths_ahead = []

    #if user selects the next choice in the decision tree
    if request.method == 'POST':
        node_id = request.POST['node_id']
        #retrieve current node in list of all nodes
        current_node = get_object_or_404(DecisionTreeNode, pk = node_id)
        nodes.append(current_node) 

        next_node = None
        if request.POST['answer']:
            #retrieve choice chosen in list of all choices
            choice_chosen = get_object_or_404(DecisionTreeChoice, choice_text = request.POST['answer'])
            #find next possible path to take based on starting node and choice taken
            path_to_take = get_object_or_404(DecisionTreePath, start_node = current_node, choice = choice_chosen)
            #next node is the end node of this path
            next_node = path_to_take.end_node
            nodes.append(next_node)
            paths_taken.append(path_to_take)

            if next_node.node_type != 'terminal':
                paths_ahead = get_list_or_404(DecisionTreePath, start_node = next_node)

        #based on current position, retrace the path taken 
        def retrieve_previous_nodes(node):
            #while the root node is not reached yet
            if node.node_type != 'root':
                prev_path = get_object_or_404(DecisionTreePath, end_node = node)
                prev_node = prev_path.start_node
                #insert previous path at the front of list of paths
                paths_taken.insert(0, prev_path)
                #insert previous node at the front of list of nodes
                nodes.insert(0, prev_node)
                #carry out this process recursively
                retrieve_previous_nodes(prev_node)
        retrieve_previous_nodes(current_node)
    
    #initial state (no path taken yet)
    else:
        nodes = [root_node]
        paths_ahead = get_list_or_404(DecisionTreePath, start_node = root_node)
    
    return render(request, 'tree.html', {'nodes': nodes, 'paths_taken': paths_taken, 'paths_ahead': paths_ahead})