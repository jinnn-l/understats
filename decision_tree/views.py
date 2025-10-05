from django.shortcuts import render, get_object_or_404, get_list_or_404

from.models import DecisionTreeNode, DecisionTreeChoice, DecisionTreePath

def decision_tree_view(request):
    #make sure only one root node present!
    root_node = get_object_or_404(DecisionTreeNode, node_type = 'root')
    nodes = []
    paths_taken = []
    paths_ahead = []

    if request.method == 'POST':
        node_id = request.POST['node_id']
        current_node = get_object_or_404(DecisionTreeNode, pk = node_id)
        nodes.append(current_node)

        next_node = None
        if request.POST['answer']:
            choice_chosen = get_object_or_404(DecisionTreeChoice, choice_text = request.POST['answer'])
            path_to_take = get_object_or_404(DecisionTreePath, start_node = current_node, choice = choice_chosen)
            next_node = path_to_take.end_node
            nodes.append(next_node)
            paths_taken.append(path_to_take)

            if next_node.node_type != 'terminal':
                paths_ahead = get_list_or_404(DecisionTreePath, start_node = next_node)

        def retrieve_previous_nodes(node):
            if node.node_type != 'root':
                prev_path = get_object_or_404(DecisionTreePath, end_node = node)
                prev_node = prev_path.start_node
                paths_taken.insert(0, prev_path)
                nodes.insert(0, prev_node)
                retrieve_previous_nodes(prev_node)
        retrieve_previous_nodes(current_node)
    
    else:
        nodes = [root_node]
        paths_ahead = get_list_or_404(DecisionTreePath, start_node = root_node)
    
    return render(request, 'tree.html', {'nodes': nodes, 'paths_taken': paths_taken, 'paths_ahead': paths_ahead})