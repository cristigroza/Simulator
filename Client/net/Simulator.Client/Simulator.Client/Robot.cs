using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Simulator.Client.CommandLayer;

namespace Simulator.Client
{
    public class Robot : IRobotActions
    {
        private readonly Lazy<ICommandLayer> _command;
        public Robot()
        {
            _command = new Lazy<ICommandLayer>(CommandFactory.CreateCommandLayer);
        }

        #region Encoders

        public short GetEncoderPulse1()
        {
            return _command.Value.GetEncoderPulse1();
        }

        public short GetEncoderPulse2()
        {
            return _command.Value.GetEncoderPulse2();
        }
        #endregion

        #region Motor control
        public void DcMotorPwmTimeCtrAll(short leftWheel, short rightWheel, short cmd3, short cmd4, short cmd5, short cmd6, short timePeriod)
        {
            _command.Value.DcMotorPwmTimeCtrAll(leftWheel, rightWheel, cmd3, cmd4, cmd5, cmd6, timePeriod);
        }

        public void DcMotorPositionTimeCtrAll(short leftWheel, short rightWheel, short cmd3, short cmd4, short cmd5, short cmd6, short timePeriod)
        {
            _command.Value.DcMotorPositionTimeCtrAll(leftWheel, rightWheel, cmd3, cmd4, cmd5, cmd6, timePeriod);
        }

        #endregion

        #region Sonars
        public short GetSensorSonar1()
        {
            return _command.Value.GetSensorSonar1();
        }

        public short GetSensorSonar2()
        {
            return _command.Value.GetSensorSonar2();
        }

        public short GetSensorSonar3()
        {
            return _command.Value.GetSensorSonar3();
        }

        public short GetSensorSonar4()
        {
            return _command.Value.GetSensorSonar4();
        }

        public short GetSensorSonar5()
        {
            return _command.Value.GetSensorSonar5();
        }

        public short GetSensorSonar6()
        {
            return _command.Value.GetSensorSonar6();
        }
        #endregion

        #region IR
        public short GetCustomAD1()
        {
            return _command.Value.GetCustomAD1();
        }

        public short GetCustomAD8()
        {
            return _command.Value.GetCustomAD8();
        }

        public short GetCustomAD2()
        {
            return _command.Value.GetCustomAD2();
        }

        public short GetSensorIRRange()
        {
            return _command.Value.GetSensorIRRange();
        }

        public short GetCustomAD3()
        {
            return _command.Value.GetCustomAD3();
        }

        public short GetCustomAD4()
        {
            return _command.Value.GetCustomAD4();
        }

        public short GetCustomAD5()
        {
            return _command.Value.GetCustomAD5();
        }

        public short GetCustomAD6()
        {
            return _command.Value.GetCustomAD6();
        }

        public short GetCustomAD7()
        {
            return _command.Value.GetCustomAD7();
        }

        #endregion
    }
}
