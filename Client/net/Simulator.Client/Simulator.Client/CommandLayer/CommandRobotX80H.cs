using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Simulator.Client.CommandLayer
{
    class CommandRobotX80H : CommandLayer
    {

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

        #region IR
        public override short GetCustomAD1()
        {
            communication.SendCommand("GetIR1;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public override short GetCustomAD8()
        {
            communication.SendCommand("GetIR1;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }


        /// <summary>
        /// Defect
        /// </summary>
        /// <returns>-1</returns>

        public override short GetCustomAD2()
        {
            communication.SendCommand("GetIR2;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public override short GetSensorIRRange()
        {
            communication.SendCommand("GetIR2;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public override short GetCustomAD3()
        {
            return -1;
        }

        public override short GetCustomAD4()
        {
            communication.SendCommand("GetIR3;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public override short GetCustomAD5()
        {
            communication.SendCommand("GetIR4;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public override short GetCustomAD6()
        {
            communication.SendCommand("GetIR5;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public override short GetCustomAD7()
        {
            communication.SendCommand("GetIR6;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        } 
        #endregion
    }
}
