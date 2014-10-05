using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Simulator.Client.CommandLayer
{
    class CommandRobotX80 : CommandLayer
    {
        public override short GetSensorSonar4()
        {
            return -1;
        }

        public override short GetSensorSonar5()
        {
            return -1;
        }

        public override short GetSensorSonar6()
        {
            return -1;
        }
    }
}
