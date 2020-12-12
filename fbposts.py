import facebook

def load_posts() :
    graph = facebook.GraphAPI(access_token="EAALsIiN8cc8BAMKnKDr4s21Ng1jFbVSYTjN7IJFq2EKmHO4OqCtMjiBf78yH1AvaEHMzOiAXVR0twOnYVJXtGD2pOitXL8F5eX2ZCEVu8jbsjPuyZCydnRl4xGA7ly74NAF0JZCgBi1YRkig18o6sD5Nee1awnXMcqjEo7RQArpjlkhaDiPnYPVXhkJ7tjTc57EInmkDVdeNDZCJ3Y6uhz6bLjgnXFXm3qsmUOWnxQZDZD", version="9.0")
    post = graph.get_object(id='me', fields='posts')
    return post['posts']['data']
