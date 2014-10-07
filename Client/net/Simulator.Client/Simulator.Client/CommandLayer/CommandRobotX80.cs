using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Simulator.Client.CommandLayer
{
    class CommandRobotX80 : CommandLayer
    {
        #region Encoders
        public override short GetSensorPot1()
        {
            return 0;
        }

        public override short GetSensorPot2()
        {
            return 0;
        }

        #endregion

        #region Sonars
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
        #endregion


      
    }
}
