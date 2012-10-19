def help( args ):
    if len( args ) > 1:
        topic = args[ 1 ]
    else:
        topic = 'help'
    topics = {
        'help': [
            '================================================================',
            'PyDerive - A symbolic derivation tool.',
            'Dionysis "dionyziz" Zindros <dionyziz@gmail.com>',
            'This software is open source and licensed under the MIT license.',
            'For more information type `help license`.',
            '================================================================',
            'Just type any function to find its derivative.',
            'Try: sin( x ), cos( x ), 3 * x, 2 * x ^ 2',
            'For more help, pick a help topic and type `help topic`:',
            '* commands',
            '* derivation',
            '* functions',
            '* license',
            '* modes',
            '* operators',
            '* symbolic',
            '* variables'
        ],
        'commands': [
            'Supported commands are:',
            '* help <topic>: Displays help information',
            '* diff <var>: Changes differentiation variable (see `help derivation`)',
            '* mode <mode>: Changes mode of operation (see `help modes`)',
            '* exit: Quits the application (you can also use Ctrl + D)',
            '* Just type an expression: Find the derivative of an algebraic expression'
        ],
        'symbolic': [
            'Derivation is symbolic, meaning that you will get a function, not a value at a specific point.',
            'For example typing sin( x ) yields cos( x ), which is not evaluated at any particular point.',
            'You can use any algebraic expression including:',
            '* Operators (see `help operators`)',
            '* Functions (see `help functions`)',
            '* Variables (see `help variables`)'
        ],
        'functions': [
            'Supported functions are: sin, cos, tan, exp, and ln.',
            'To embed a function in an algebraic expression, simply type it with parentheses around its argument.',
            'For example sin( x ) or sin( 5 + x ).',
            'Custom functions or arbitrary functions such as "f" are not supported.',
            '"f" will be treated as a variable, not a function (see `help variables`).'
        ],
        'operators': [
            'Supported operators are: +, -, *, /, ^.',
            'Notice that not all traditional Python operators are supported.',
            'For example, ** which traditionally means power in Python is not supported.',
            'The order of operators is as in usual math. You can use ( parentheses ) for grouping.',
            'Multiplication must be specified explicitly, so 3x must be written as 3 * x.'
        ],
        'derivation': [
            'Derivation is done with respect to variable x.',
            'All other variables are treated as constants.',
            'To change the variable which derivation is done with respect to, use the `diff` command:',
            'Type `diff y` where "y" is the variable with respect to which you wish to differentiate.',
            'All variables must be one small latin letter, a - z.'
        ],
        'variables': [
            'Variables are small latin letters a - z. By default, you are differentiating with respect to x.',
            'See `help derivation` to learn how to change that.',
            'All variables except the variable with respect to which you are differentiating are treated as constants.',
        ],
        'license': [
            'Copyright (C) 2012 Dionysis "dionyziz" Zindros <dionyziz@gmail.com>',
            '',
            'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:',
            '',
            'The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.',
            '',
            'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'
        ],
        'modes': [
            'Modes allow different modes of operation for the symbolic tool.',
            'While the main functionality of the application is to handle derivation, there are a few other things it can do.',
            'Here are all the modes:',
            '* derive: Differentiates the expression you type and simplifies the result. This is the default mode.',
            '* simplify: Only simplifies the expression you type. Does not differentiate.',
            '* derive-only: Differentiate the expression, but do not simplify the result.',
            '* parse: Only parse the given expression. Do not change it in any way. Do not differentiate or simplify.',
            'To change modes type `mode x` where x is your desired mode.',
            'For example `mode parse` switches to parse mode.'
        ]
    }
    if topic not in topics:
        topic = 'help'
    print '\n'.join( topics[ topic ] )
