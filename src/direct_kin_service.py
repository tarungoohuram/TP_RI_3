#!/usr/bin/env python

from TP_RI_3.srv import *
import rospy
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list



class groupService:

	def __init__(self):
		rospy.init_node('finger_service_server')
		self.group_name = rospy.get_param('~group_name',"Middle")
		print self.group_name
		moveit_commander.roscpp_initialize(sys.argv)

		self.robot=moveit_commander.RobotCommander()
		self.scene =moveit_commander.PlanningSceneInterface()
		self.move_group =moveit_commander.MoveGroupCommander(self.group_name)
		rospy.Service('direct_kin_service_%s'%(self.group_name), direct_kin_service, self.handle_req)
		rospy.spin()


	def handle_req(self,req):
		try:
			print req
			joint_goal = self.move_group.get_current_joint_values()
			joint_goal[0] = req.joint1.data
			joint_goal[1] = req.joint2.data
			if len(joint_goal)>2:
				joint_goal[2] = req.joint3.data
			self.move_group.go(joint_goal, wait=True)
			self.move_group.stop()
			rep=direct_kin_serviceResponse()
			rep.res.data=True
			rep.message.data="Success"
			return rep
		except Exception as e:
			rep=direct_kin_serviceResponse()
			print e
			return rep

if __name__ == "__main__":
	groupService()