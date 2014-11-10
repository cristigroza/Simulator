using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using Simulator.Client;

namespace Simulator.Sample
{
    public partial class Form1 : Form
    {
        private readonly Robot _robot;
        public Form1()
        {
            InitializeComponent();
            _robot = new Robot();
            RobotConfiguration.RobotType = EnumRobotType.X80;
            _robot.StandardSensorEvent += _robot_StandardSensorEvent;
        }

        void _robot_StandardSensorEvent(object sender, EventArgs e)
        {
            RobotSensorReadings.Ir1 = _robot.GetSensorIRRange();
            RobotSensorReadings.Ir2 = _robot.GetCustomAD3();
            RobotSensorReadings.Ir3 = _robot.GetCustomAD4();
            RobotSensorReadings.Ir4 = _robot.GetCustomAD5();
            RobotSensorReadings.Ir5 = _robot.GetCustomAD6();
            RobotSensorReadings.Ir6 = _robot.GetCustomAD7();
            RobotSensorReadings.Ir7 = _robot.GetCustomAD8();

            RobotSensorReadings.Sonar1 = _robot.GetSensorSonar1();
            RobotSensorReadings.Sonar2 = _robot.GetSensorSonar2();
            RobotSensorReadings.Sonar3 = _robot.GetSensorSonar3();
            RobotSensorReadings.Sonar4 = _robot.GetSensorSonar4();
            RobotSensorReadings.Sonar5 = _robot.GetSensorSonar5();
            RobotSensorReadings.Sonar6 = _robot.GetSensorSonar6();

            RobotSensorReadings.Encoder1 = _robot.GetEncoderPulse1();
            RobotSensorReadings.Encoder2 = _robot.GetEncoderPulse2();


            this.BeginInvoke((Action)(() =>
            {
                this.txtIR1.Text = RobotSensorReadings.Ir1.ToString();
                this.txtIR2.Text = RobotSensorReadings.Ir2.ToString();
                this.txtIR3.Text = RobotSensorReadings.Ir3.ToString();
                this.txtIR4.Text = RobotSensorReadings.Ir4.ToString();
                this.txtIR5.Text = RobotSensorReadings.Ir5.ToString();
                this.txtIR6.Text = RobotSensorReadings.Ir6.ToString();
                this.txtIR7.Text = RobotSensorReadings.Ir7.ToString();

                this.txtS1.Text = RobotSensorReadings.Sonar1.ToString();
                this.txtS2.Text = RobotSensorReadings.Sonar2.ToString();
                this.txtS3.Text = RobotSensorReadings.Sonar3.ToString();
                this.txtS4.Text = RobotSensorReadings.Sonar4.ToString();
                this.txtS5.Text = RobotSensorReadings.Sonar5.ToString();
                this.txtS6.Text = RobotSensorReadings.Sonar6.ToString();

                this.txtEncoder1.Text = RobotSensorReadings.Encoder1.ToString();
                this.txtEncoder2.Text = RobotSensorReadings.Encoder2.ToString();
            }));
        }

        private void btnStartRobot_Click(object sender, EventArgs e)
        {
            _robot.EnableStandardSensorSending();
        }

        private void btnForward_Click(object sender, EventArgs e)
        {
            _robot.DcMotorPositionTimeCtrAll((short)(RobotSensorReadings.Encoder1 + 1000), (short)(RobotSensorReadings.Encoder1 + 1000), 0, 0, 0, 0, 1000);
        }

        private void btnBack_Click(object sender, EventArgs e)
        {
            _robot.DcMotorPositionTimeCtrAll((short)(RobotSensorReadings.Encoder1 - 1000), (short)(RobotSensorReadings.Encoder2 - 1000), 0, 0, 0, 0, 1000);
        }

        private void btnLeft_Click(object sender, EventArgs e)
        {
            _robot.DcMotorPositionTimeCtrAll((short)(RobotSensorReadings.Encoder1), (short)(RobotSensorReadings.Encoder2 + 1000), 0, 0, 0, 0, 1000);
        }

        private void btnRight_Click(object sender, EventArgs e)
        {
            _robot.DcMotorPositionTimeCtrAll((short)(RobotSensorReadings.Encoder1 + 1000), (short)(RobotSensorReadings.Encoder2), 0, 0, 0, 0, 1000);
        }
    }
}
