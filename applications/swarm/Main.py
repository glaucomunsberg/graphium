import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', type=str, default="", help='try the mode reader or swarm')
    # Reader
    parser.add_argument('--osm_path', type=str, default="city_pelotas/ex_pelotas.osm", help='path do city.osm')
    # Swarm
    parser.add_argument('--swarm_identifier', type=str, default=None,
                        help='Identifier of swarm. Empty the instance will be created else get information from db')
    parser.add_argument('--swarm_name', type=str, default=None, help='name of swarm. If empty full with datatime')
    parser.add_argument('--user_email', type=str, default="admin@graphium.com", help='Email to identify the user')
    parser.add_argument('--swarm_num_agent', type=int, default=3, help='Number of agents to work')
    parser.add_argument('--swarm_city', type=str, default=None, help='City to crawler')
    parser.add_argument('--model_name', type=str, default=None, help='Model use on prediction')
    parser.add_argument('--rake', type=str, default=None, help='Functions to view')
    parser.add_argument('--id', type=str, default=None, help='Identified')

    args = parser.parse_args()

    mode = None
    if args.mode == "reader":
        from assistant.Reader import Reader
        mode = Reader(args)
    elif args.mode == "swarm":
        from hive.Swarm import Swarm
        mode = Swarm(args)
    elif args.mode == "assessor":
        from system.Assessor import Assessor
        mode = Assessor(args)

    elif args.mode == "marionette":
        from hive.Marionette import Marionette
        mode = Marionette(args)
    else:
        None
        # mode = Compiler(args)

    if mode is None:
        print 'Empty Mode Param'
    else:
        mode.start()


if __name__ == '__main__':
    main()
