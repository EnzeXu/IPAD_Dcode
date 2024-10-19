#!/bin/bash
# Navigate to the workspace
cd /data2/enze/workspace/Invariant_Physics

# Check if the tmux session exists
tmux has-session -t friction_pendulum_default_2_4_0-9 2>/dev/null

if [ $? != 0 ]; then
  tmux new-session -d -s friction_pendulum_default_2_4_0-9

  tmux send-keys -t friction_pendulum_default_2_4_0-9 "source venv/bin/activate" C-m
  tmux send-keys -t friction_pendulum_default_2_4_0-9 "bash jobs/job_20241001_friction_pendulum_default_2_4_seed=0-9.sh" C-m
  echo "Launched jobs/job_20241001_friction_pendulum_default_2_4_seed=0-9.sh at friction_pendulum_default_2_4_0-9"
  # If you want to leave the session detached, remove the line below
  # tmux send-keys -t friction_pendulum_default_2_4_0-9 "exit" C-m
else
  echo "Session 'friction_pendulum_default_2_4_0-9' already exists. Attaching..."
  tmux attach -t friction_pendulum_default_2_4_0-9
  tmux send-keys -t friction_pendulum_default_2_4_0-9 "source venv/bin/activate" C-m
  tmux send-keys -t friction_pendulum_default_2_4_0-9 "bash jobs/job_20241001_friction_pendulum_default_2_4_seed=0-9.sh" C-m
fi
