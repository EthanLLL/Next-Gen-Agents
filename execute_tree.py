def execute_tree(tree, function_map):
    # if Tree is empty
    if not tree:
        return 'No functions to execute'

    # if 'source' key in current node, means this node depends on a function
    if "source" in tree:
        source_node = tree["source"]
        if source_node["type"] == "function":

            function_name = source_node["name"]
            function = function_map.get(function_name)
            if function:
                # 获取函数参数
                function_kwargs = {}
                for arg_node in source_node.get("arguments", []):
                    arg_name = arg_node["name"]
                    arg_value = execute_tree(arg_node, function_map)
                    function_kwargs[arg_name] = arg_value
                # 执行函数并获取结果
                result = function(**function_kwargs)
                return result
            else:
                raise ValueError(f"Function '{function_name}' not found in the function map.")
    
    # No 'source' key, 
    node_name = tree["name"]
    if node_name in function_map:
        # 从函数映射字典中获取函数
        function = function_map[node_name]
        # 获取函数参数
        function_kwargs = {}
        for arg_node in tree.get("arguments", []):
            arg_name = arg_node["name"]
            arg_value = execute_tree(arg_node, function_map)
            function_kwargs[arg_name] = arg_value
        # 执行函数并传递参数
        result = function(**function_kwargs)
        return result
    
    # 如果节点是一个值,直接返回值
    if "value" in tree:
        return tree["value"]