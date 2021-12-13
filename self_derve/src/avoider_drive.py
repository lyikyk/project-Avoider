#!/home/pi/.pyenv/versions/SD/bin/python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher

    def lds_callback(self, scan):
        # scan 분석 후 속도 결정
        print(f'scan[30]:{scan.ranges[45]:.3f}')
        print(f'scan[-30]:{scan.ranges[-45]:.3f}')		
        turtle_vel = Twist()
         # 전진 속도 및 회전 속도 지정
        if scan.ranges[0] > 0.25 or scan.ranges[0] == 0.0:
            turtle_vel.linear.x = 0.15
        else:
            turtle_vel.linear.x = 0.0
            if scan.ranges[30] < 0.25 or scan.ranges[30] != 0:
                if scan.ranges[-30] < 0.25:
                    turtle_vel.angular.z = -2
                else:
                    turtle_vel.angular.z = 2
            elif scan.ranges[-30] < 0.25 or scan.ranges[-30] != 0:
                if scan.ranges[30] < 0.25:
                    turtle_vel.angular.z = 2
                else:
                    turtle_vel.angular.z = -2
        if scan.ranges[30] < 0.25 and scan.ranges[30] != 0:
            turtle_vel.linear.x = 0
            turtle_vel.angular.z = -1
        if scan.ranges[-30] < 0.25 and scan.ranges[-30] != 0:
            turtle_vel.linear.x = 0
            turtle_vel.angular.z = 1
        

         # 속도 출력
        self.publisher.publish(turtle_vel)

def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()

if __name__ == "__main__":
    main()
