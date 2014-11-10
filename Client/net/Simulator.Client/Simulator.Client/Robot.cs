using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Text;

using System.Threading.Tasks;
using System.Timers;
using Simulator.Client.CommandLayer;

namespace Simulator.Client
{
    public class Robot : IRobotActions
    {
        private object _lockObj = new object();
        private readonly Lazy<ICommandLayer> _command;
        private readonly Timer _standardSensorTimer;
        private readonly Timer _customSensorTimer;
        private readonly Timer _motorSensorTimer;

        public Robot()
        {
            _command = new Lazy<ICommandLayer>(CommandFactory.CreateCommandLayer);
            _customSensorTimer = new Timer(50);
            _customSensorTimer.Elapsed += OnCustomSensorEvent;
          

            _motorSensorTimer = new Timer(50);
            _motorSensorTimer.Elapsed += OnMotorSensorEvent;
           

            _standardSensorTimer = new Timer(50);
            _standardSensorTimer.Elapsed += OnStandardSensorEvent;
            

        }

      

        public void connectRobot(string robot)
        {

        }

        public void EnableStandardSensorSending()
        {
            _customSensorTimer.Enabled = true;
            _motorSensorTimer.Enabled = true;
            _standardSensorTimer.Enabled = true;
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

        public void SuspendDcMotor(short channel)
        {

        }

        public void DisableDcMotor(short channel)
        {

        }

        public void SetDcMotorControlMode(short channel, short controlMode)
        {

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

        private void OnStandardSensorEvent(object sender, ElapsedEventArgs e)
        {
            lock (_lockObj)
            {
                OnStandardSensorEvent();
            }
           
        }

        private void OnMotorSensorEvent(object sender, ElapsedEventArgs e)
        {
            lock (_lockObj)
            {
                OnMotorSensorEvent();
            }
        }

        private void OnCustomSensorEvent(object sender, ElapsedEventArgs e)
        {
            lock (_lockObj)
            {
                OnCustomSensorEvent();
            }
        }


        #endregion



    }
}
