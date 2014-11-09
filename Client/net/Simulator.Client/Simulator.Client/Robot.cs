using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Simulator.Client.CommandLayer;

namespace Simulator.Client
{
    public class Robot : IRobotActions
    {
        private readonly Lazy<ICommandLayer> _command;
        private readonly Timer _standardSensorTimer;
        private readonly Timer _customSensorTimer;
        private readonly Timer _motorSensorTimer;
        public Robot()
        {
            _command = new Lazy<ICommandLayer>(CommandFactory.CreateCommandLayer);

            _customSensorTimer = new Timer(OnCustomSensorEvent, null, 50, 50);
            _motorSensorTimer = new Timer(OnMotorSensorEvent, null, 50, 50);
            _standardSensorTimer = new Timer(OnStandardSensorEvent, null, 50, 50);
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
        public short GetSensorPot1()
        {
            return _command.Value.GetSensorPot1();
        }

        public short GetSensorPot2()
        {
            return _command.Value.GetSensorPot2();
        }
        #endregion

        #region Motor control

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


        public short GetCustomAD8()
        {
            return _command.Value.GetCustomAD8();
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

        #region Events


        public event EventHandler MotorSensorEvent;
        public event EventHandler StandardSensorEvent;
        public event EventHandler CustomSensorEvent;

        protected virtual void OnStandardSensorEvent()
        {
            EventHandler handler = StandardSensorEvent;
            if (handler != null) handler(this, EventArgs.Empty);
        }
        protected virtual void OnMotorSensorEvent()
        {
            EventHandler handler = MotorSensorEvent;
            if (handler != null) handler(this, EventArgs.Empty);
        }
        protected virtual void OnCustomSensorEvent()
        {
            EventHandler handler = CustomSensorEvent;
            if (handler != null) handler(this, EventArgs.Empty);
        }

        private void OnCustomSensorEvent(object state)
        {
            this.OnCustomSensorEvent();
        }
        private void OnMotorSensorEvent(object state)
        {
            this.OnMotorSensorEvent();
        }
        private void OnStandardSensorEvent(object state)
        {
            this.OnStandardSensorEvent();
        }


        #endregion
    }
}
