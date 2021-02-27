import Commands.todos


# Map command name to command function
commandsDict = {
    'add': todos.addItem,
    'ls': todos.showItems,
    'del': todos.deleteItem,
    'done': todos.completeItem,
    'report': todos.stats,
}
