#!/usr/bin/env python
package_name='collision_checking'
import roslib; roslib.load_manifest(package_name)
import argparse, herbpy, openravepy

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run the benchmark tests")
    parser.add_argument("--outfile", type=str, default=None,
                        help="The output file to save results in, if none results are not saved")
    parser.add_argument("--env", type=str, default=None,
                        help="The environment to load")
    parser.add_argument("--body", type=str, default="herb",
                        help="The kinbody to move around for collision checking")
    parser.add_argument("--test", type=str, default=None,
                        help="The list of poses to check, this should be in the form of a results file from a previous run")
    parser.add_argument("--duration", type=float, default=5.0,
                        help="The duration to run the benchmark. Poses will be sampled and collision checks will be run until the total time spent collision checking exceeds this duration.")
    parser.add_argument("--extent", type=float, default=2.0,
                        help="The edge length for the cube from which poses will be sampled.")

    args = parser.parse_args()

    # Load the environment
    if args.body == 'herb':
        env, robot = herbpy.initialize(sim=True)
    else:
        env = openravepy.Environment()

    if args.env:
        env.Load(args.env)
        
    # Verify the kinbody is in the environment
    body = env.GetKinBody(args.body)
    if body is None:
        raise Exception('No body with name %s in environment. Failing.' % args.body)

    # Load the openrave module
    try:
        module = openravepy.RaveCreateModule(env, 'collisioncheckingbenchmark')
    except openravepy.openrave_exception:
        raise Exception('Unable to load CollisionCheckingBenchmark module. Check your OPENRAVE_PLUGINS environment variable.')

    # Generate the parameters
    params = {}
    params['body'] = str(body.GetName())
    params['duration'] = args.duration
    if args.outfile is not None:
        params['outfile'] = args.outfile
    params['extent'] = args.extent

    result = module.SendCommand("Run " + str(params))
