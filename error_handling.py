def error_handling(exc_type, exc_value, exc_traceback):
    print("Traceback (most recent call last):")
    while exc_traceback:
        print("  File \"{}\", line {}, in {}".format(exc_traceback.tb_frame.f_code.co_filename,
                                                     exc_traceback.tb_lineno,
                                                     exc_traceback.tb_frame.f_code.co_name))
        exc_traceback = exc_traceback.tb_next

def main():
    # Your main code here
    pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occurred: {}".format(e))
        error_handling(type(e), e, e.__traceback__)