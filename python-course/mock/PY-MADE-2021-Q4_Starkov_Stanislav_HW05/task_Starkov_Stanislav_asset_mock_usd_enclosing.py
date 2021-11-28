  iterations = [0, 1, 2, 3, 4]
  def calculate_used_for_iteration() -> float:
      return 76.32 + (0.1 * iterations.pop())
  mock_get_usd_course.side_effect = calculate_used_for_iteration
