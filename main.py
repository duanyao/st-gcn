#!/usr/bin/env python
import argparse
import sys



if __name__ == '__main__':
    # openpose should be imported before torch/torchlight, otherwise GPU memory usage would be increased by 270MB
    preParser = argparse.ArgumentParser()
    preParser.add_argument('--openpose', default=None)
    arg, unknown = preParser.parse_known_args()
    if arg.openpose is not None:
        # print('main: importing openpose from ' + arg.openpose)
        sys.path.append('{}/python'.format(arg.openpose))
    try:
        from openpose import pyopenpose
    except:
        pass

    # torchlight
    import torchlight
    from torchlight import import_class

    parser = argparse.ArgumentParser(description='Processor collection')

    # region register processor yapf: disable
    processors = dict()
    processors['recognition'] = import_class('processor.recognition.REC_Processor')
    processors['demo_old'] = import_class('processor.demo_old.Demo')
    processors['demo'] = import_class('processor.demo_realtime.DemoRealtime')
    processors['demo_offline'] = import_class('processor.demo_offline.DemoOffline')
    #endregion yapf: enable

    # add sub-parser
    subparsers = parser.add_subparsers(dest='processor')
    for k, p in processors.items():
        subparsers.add_parser(k, parents=[p.get_parser()])

    # read arguments
    arg = parser.parse_args()

    # start
    Processor = processors[arg.processor]
    p = Processor(sys.argv[2:])

    p.start()
