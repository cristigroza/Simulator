using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Simulator.Client
{
    public interface IRobotActions
    {
        #region Encoders
        ///<summary>
        /// Left wheel encoder value.
        ///</summary>
        short GetEncoderPulse1();

        ///<summary>
        /// Right wheel encoder value.
        ///</summary>
        short GetEncoderPulse2();

        #endregion

        //TODO Test if the parameters match the wheels control on the robot
        void DcMotorPwmTimeCtrAll(short leftWheel, short rightWheel, short cmd3, short cmd4, short cmd5, short cmd6, short timePeriod);
        void DcMotorPositionTimeCtrAll(short leftWheel, short rightWheel, short cmd3, short cmd4, short cmd5, short cmd6, short timePeriod);

        #region Sonars
        ///<summary>
        /// Left
        ///</summary>
        short GetSensorSonar1();

        ///<summary>
        /// Front
        ///</summary>
        short GetSensorSonar2();

        ///<summary>
        /// Right
        ///</summary>
        short GetSensorSonar3();
        short GetSensorSonar4();
        short GetSensorSonar5();
        short GetSensorSonar6();
        #endregion

        #region Ir
        ///<summary>
        /// Left
        ///</summary>
        short GetCustomAD1();
        short GetCustomAD8();
        ///<summary>
        /// Left down
        ///</summary>
        short GetCustomAD2();
        short GetSensorIRRange();
        ///<summary>
        /// Left up
        ///</summary>
        short GetCustomAD3();

        ///<summary>
        /// Right Up
        ///</summary>
        short GetCustomAD4();
        ///<summary>
        /// Right down
        ///</summary>
        short GetCustomAD5();
        ///<summary>
        /// Right
        ///</summary>
        short GetCustomAD6();
        ///<summary>
        /// Rear
        ///</summary>
        short GetCustomAD7();

        #endregion
    }
}
