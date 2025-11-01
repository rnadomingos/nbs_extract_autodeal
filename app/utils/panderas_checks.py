import pandera as pa

def check_output_with(schema, lazy: bool):
    def decorator_check_output(func):
        return pa.check_output(schema=schema,lazy=lazy)(func)
    return decorator_check_output