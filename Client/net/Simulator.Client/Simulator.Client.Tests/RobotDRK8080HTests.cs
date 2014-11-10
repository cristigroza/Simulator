using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using NUnit.Framework;

namespace Simulator.Client.Tests
{
    [TestFixture]
    public class RobotDRK8080Tests
    {
        public RobotDRK8080Tests()
        {
            _robot = new Robot();

            RobotConfiguration.RobotType = EnumRobotType.Drk8080;
        }
        private Robot _robot;

        [TearDown]
        public void Dispose()
        {
            _robot.DcMotorPositionTimeCtrAll(0, 0, 0, 0, 0, 0, 1000);
        }


        [Test]
        public void Move_Robot_Forward_Using_PositionTimeCtr()
        {
            _robot.DcMotorPositionTimeCtrAll(10000, 10000, 0, 0, 0, 0, 1000);

        }
        [Test]
        public void Move_Robot_Backwards_Using_PositionTimeCtr()
        {
            _robot.DcMotorPositionTimeCtrAll(30000, 30000, 0, 0, 0, 0, 1000);
        }

        [Test]
        public void Rotate_Robot_To_Left_Using_PositionTimeCtr()
        {
            _robot.DcMotorPositionTimeCtrAll(0, 10000, 0, 0, 0, 0, 1000);
        }

        [Test]
        public void Rotate_Robot_To_Right_Using_PositionTimeCtr()
        {
            _robot.DcMotorPositionTimeCtrAll(10000, 0, 0, 0, 0, 0, 1000);
        }


        [Test]
        public void Read_Robot_Ir_Senfors()
        {
            _robot.GetCustomAD3();
            _robot.GetCustomAD4();
            _robot.GetCustomAD5();
            _robot.GetCustomAD6();
            _robot.GetCustomAD7();
            _robot.GetCustomAD8();
            _robot.GetSensorIRRange();
        }

        [Test]
        public void Read_Robot_Sonar_Sensors()
        {
            _robot.GetSensorSonar1();
            _robot.GetSensorSonar2();
            _robot.GetSensorSonar3();
            _robot.GetSensorSonar4();
            _robot.GetSensorSonar5();
            _robot.GetSensorSonar6();
        }

        [Test]
        public void Read_Robot_Encoders()
        {
            _robot.GetEncoderPulse1();
            _robot.GetSensorPot1();
            _robot.GetEncoderPulse2();
            _robot.GetSensorPot2();
            
        }

        [Test]
        public void Events()
        {
            _robot.CustomSensorEvent += _robot_CustomSensorEvent;
            _robot.StandardSensorEvent += _robot_StandardSensorEvent;
            _robot.MotorSensorEvent += _robot_MotorSensorEvent;
            while (true)
            {

            }
        }

        void _robot_MotorSensorEvent(object sender, EventArgs e)
        {

        }
        private object _sensors = new object();
        void _robot_StandardSensorEvent(object sender, EventArgs e)
        {
            lock (_sensors)
            {


                _robot.GetSensorSonar1();
                _robot.GetSensorSonar2();
                _robot.GetSensorSonar3();
                _robot.GetSensorSonar4();
                _robot.GetSensorSonar5();
            }
        }

        void _robot_CustomSensorEvent(object sender, EventArgs e)
        {

        }

        [Test]
        public void RotateAction()
        {
            int left;
            int right;
            while (true)
            {

                left = _robot.GetSensorPot1();
                right = _robot.GetSensorPot2();
                

                left += 3000;
                right += 3000;

                _robot.DcMotorPositionTimeCtrAll((short)left, (short)right, 0, 0, 0, 0, 1000);
            }
        }





    }
}
