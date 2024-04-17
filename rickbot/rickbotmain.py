import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import argparse
import os
import time

import pysrt


# take arguments from the command line with 1) input file (String)
parser = argparse.ArgumentParser(description='Streams srt subtitles to specified ros topic')
parser.add_argument('input_file', type=str, help='path to the input srt file')
# 2) ros arguments
parser.add_argument('ros_args', nargs=argparse.REMAINDER)
args = parser.parse_args()


INPUT_FILE = args.input_file
PATH_OF_THIS_FILE = os.path.dirname(os.path.realpath(__file__))
class SubtitleNode(Node):
    def __init__(self):
        super().__init__('rickbot')

        self.publisher_ = self.create_publisher(String, '/chatter', 10)
        self.timer_ = self.create_timer(0.1, self.publish_subtitle)
        try:
            self.subs = pysrt.open(INPUT_FILE)
        except:
            self.get_logger().error("Could not open file: " + INPUT_FILE)
            # try adding current folder to the input file
            try: 
                self.subs = pysrt.open(os.path.join(PATH_OF_THIS_FILE, INPUT_FILE))
                print("Opened file: " + os.path.join(PATH_OF_THIS_FILE, INPUT_FILE))
            except:
                self.get_logger().error("Could not open file: " + os.path.join(PATH_OF_THIS_FILE, INPUT_FILE))
                return
        self.current_index_ = 0

        self.timestamp_start_loop = time.time()
        self.timestamp_absolute_start = time.time()
        self.total_loops = 0

    def publish_subtitle(self):
        # Check if it is time to publish a new subtitle
        now = time.time()

        passed_time = now - self.timestamp_start_loop
        next_timestamp = self.subs[self.current_index_].start.to_time()
        next_timestamp_seconds = next_timestamp.hour*3600 + next_timestamp.minute*60 + next_timestamp.second

        if passed_time < next_timestamp_seconds:
            return

        text_ = self.subs[self.current_index_].text
        # Remove all nextline characters or newlines
        text_ = text_.replace('\n', ' ')
        text_ = text_.replace('\r', ' ')

        self.publisher_.publish(String(data=text_))
        
        # Print timestamp, index and subtitle
        print("Timestamp: " + str(self.subs[self.current_index_].start.to_time()) + ", index: " + str(self.current_index_) + ", subtitle: " + text_)
        
        self.current_index_ += 1
        if self.current_index_ >= len(self.subs):
            self.current_index_ = 0
            self.timestamp_start_loop = time.time()

            self.total_loops += 1
            # Print time passed since start of the program and total loops
            print("Time passed since start of the program: " + str(time.time() - self.timestamp_absolute_start) + ", total loops: " + str(self.total_loops))

def main(args=None):
    rclpy.init(args=args)
    subtitle_node = SubtitleNode()
    rclpy.spin(subtitle_node)
    subtitle_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
