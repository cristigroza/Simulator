using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Simulator.Client.CommandLayer
{
    class CommandRobotDRK8080 : CommandLayer
    {

        #region Encoders
        public override short GetEncoderPulse1()
        {
            return 0;
        }

        public override short GetEncoderPulse2()
        {
            return 0;
        }

        #endregion

        #region Sonars
        public override short GetSensorSonar6()
        {
            return 255;
        }  
        #endregion

        #region IR
      

        public override short GetCustomAD8()
        {
            return -1;
        }

      

        public override short GetSensorIRRange()
        {
            return -1;
        }

        public override short GetCustomAD3()
        {
            return -1;
        }

        public override short GetCustomAD4()
        {
            return -1;
        }

        public override short GetCustomAD5()
        {
            return -1;
        }

        public override short GetCustomAD6()
        {
            return -1;
        }

        public override short GetCustomAD7()
        {
            return -1;
        }
        #endregion
    }
}
