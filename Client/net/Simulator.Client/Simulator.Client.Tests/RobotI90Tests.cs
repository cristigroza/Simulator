using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using NUnit.Framework;

namespace Simulator.Client.Tests
{
    [TestFixture]
    public class RobotI90Tests
    {
        public RobotI90Tests()
        {
            _robot = new Robot();

            RobotConfiguration.RobotType = EnumRobotType.I90;
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
        public void Move_Robt_Forward_Using_PWMTImeCtrl()
        {
            _robot.DcMotorPwmTimeCtrAll(32000, 32000, 0, 0, 0, 0, 1000);
        }

        [Test]
        public void Move_Robot_Backwards_Using_PWMTImeCtrl()
        {

            _robot.DcMotorPwmTimeCtrAll(16000, 16000, 0, 0, 0, 0, 1000);
        }

        [Test]
        public void Rotate_Robot_To_Left_Using_PWMTImeCtrl()
        {
            _robot.DcMotorPwmTimeCtrAll(0, 32000, 0, 0, 0, 0, 1000);
        }

        [Test]
        public void Rotate_Robot_To_Right_Using_PWMTImeCtrl()
        {
            _robot.DcMotorPwmTimeCtrAll(32000, 0, 0, 0, 0, 0, 1000);
        }



        [Test]
        public void Read_Robot_Ir_Senfors()
        {

            _robot.GetCustomAD1();
            _robot.GetCustomAD2();
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
            _robot.GetEncoderPulse2();
        }













    }
}
