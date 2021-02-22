# helper function( decorator and function )
import time



def print_time(arg):
    """
        print({start} {end} {comsumed time})
    """
    if callable(arg): # if it is function 
        def wrapper(*args, **kwargs):
            start = time.time()
            arg(*args, **kwargs)
            end = time.time()
            print("start_time : {} | end time : {} | consume time | : {}".format(start, end, end - start))
        return wrapper
    else :  
        def wrapper(f):
            def ref_f(*args, **kwargs):
                start = time.time()
                reval = f(*args, **kwargs)
                end = time.time()
                print(arg.format(start, end, end-start))
            
                return reval
            return ref_f
        return wrapper