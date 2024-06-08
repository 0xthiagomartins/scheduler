from nameko.standalone.rpc import ClusterRpcProxy

config = {"AMQP_URI": "amqp://guest:guest@localhost"}

with ClusterRpcProxy(config) as rpc:
    rpc.scheduler_service.add_job(
        "print_hello", 10, "seconds", lambda: print("Hello, world!")
    )
    print(rpc.scheduler_service.list_jobs())
    rpc.scheduler_service.remove_job("print_hello")
