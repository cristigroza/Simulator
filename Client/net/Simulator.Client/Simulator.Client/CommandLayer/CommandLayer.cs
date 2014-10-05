using System;
using System.Runtime.InteropServices;

namespace Simulator.Client.CommandLayer
{
    class CommandLayer : ICommandLayer
    {
        protected readonly Communication communication;
        public CommandLayer()
        {
            communication = new Communication();

        }


        #region Encoders
        public virtual short GetEncoderPulse1()
        {
            communication.SendCommand("getLeftWheelEncoderValue;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetEncoderPulse2()
        {
            communication.SendCommand("getRightWheelEncoderValue;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }
        
        #endregion

        #region Motors
        public virtual void DcMotorPwmTimeCtrAll(short leftWheel, short rightWheel, short cmd3, short cmd4, short cmd5, short cmd6, short timePeriod)
        {
            communication.SendCommand(string.Format("DcMotorPwmTimeCtrAll;{0};{1};{2}", leftWheel, rightWheel, timePeriod / 1000));
            communication.GetCommand();
        }

        public virtual void DcMotorPositionTimeCtrAll(short leftWheel, short rightWheel, short cmd3, short cmd4, short cmd5, short cmd6, short timePeriod)
        {
            communication.SendCommand(string.Format("DcMotorPositionTimeCtrAll;{0};{1};{2}", leftWheel, rightWheel, timePeriod / 1000));
            communication.GetCommand();
        } 
        #endregion

        #region Sonars
        public virtual short GetSensorSonar1()
        {
            communication.SendCommand("GetSensorSonar1;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetSensorSonar2()
        {
            communication.SendCommand("GetSensorSonar2;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetSensorSonar3()
        {
            communication.SendCommand("GetSensorSonar3;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetSensorSonar4()
        {
            communication.SendCommand("GetSensorSonar4;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetSensorSonar5()
        {
            communication.SendCommand("GetSensorSonar5;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetSensorSonar6()
        {
            communication.SendCommand("GetSensorSonar6;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        } 
        #endregion

        #region IR
        public virtual short GetCustomAD1()
        {
            communication.SendCommand("GetIR1;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetCustomAD8()
        {
            communication.SendCommand("GetIR1;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetCustomAD2()
        {
            communication.SendCommand("GetIR2;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetSensorIRRange()
        {
            communication.SendCommand("GetIR2;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetCustomAD3()
        {
            communication.SendCommand("GetIR3;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetCustomAD4()
        {
            communication.SendCommand("GetIR4;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetCustomAD5()
        {
            communication.SendCommand("GetIR5;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetCustomAD6()
        {
            communication.SendCommand("GetIR6;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        }

        public virtual short GetCustomAD7()
        {
            communication.SendCommand("GetIR7;");
            var ret = communication.GetCommand();
            return Int16.Parse(ret);
        } 
        #endregion
    }
}
