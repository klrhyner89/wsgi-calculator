#!/usr/bin/env python
import traceback
"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
def homepage():
    page = '''
  <h1>This is a simple Whiskey Calculator</h1>
  <h2>it can add, subtract, multiply, and divide</h2>
  <h2>to use, type something simlar to the following in the URL bar</h2>
  <h3>http://localhost:8080/add/15/10</h3>
  '''
    return page

def operation(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    # sum = "0"
    operations = {'': homepage,
             'add': '+',
             'subtract': '-',
             'multiply': '*',
             'divide': '/',
             }
    try:
      if args[0] == '':
        return operations[args[0]]()
      # args[0] = 'add', args[1] = num_1, args[2] = num_2
      head = '<h4>The solution to your request is:</h4>'
      solution = f'<h2>{str(int(eval(args[1] + operations[args[0]] + args[2])))}</h2>'
      foot = '<a href="/">Back to home</a>'
    except KeyError:
      raise NameError
    return '\r\n'.join([head, solution, foot])

# TODO: Add functions for handling more arithmetic operations.

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    # e.g.
    # func = add
    # args = ['25', '32']
    args = path.strip('/').split('/')
    return args

#environ is provided by wsgiref, does not need to be imported like os.environ
def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        # print(path)
        if path is None:
            raise NameError
        args = resolve_path(path)
        status = '200 OK'
        body = operation(*args)
    except NameError:
        status = '404 Not Found'
        body = '<h1>Not Found</h1>'
    except Exception:
        status = '500 Internal Server Error'
        body = '<h1>Internal Server Error</h1>'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-type', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]
    # pass

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
    # pass
