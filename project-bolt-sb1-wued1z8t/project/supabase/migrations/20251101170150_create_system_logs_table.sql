/*
  # Smart Rear-View System - System Logs Table

  1. New Tables
    - `system_logs`
      - `id` (uuid, primary key) - Unique identifier for each log entry
      - `timestamp` (timestamptz) - When the event occurred
      - `event_type` (text) - Type of event (INDICATOR, REVERSE, AI_DETECTION, WARNING, SYSTEM)
      - `details` (text) - Detailed description of the event
      - `camera_view` (text, nullable) - Active camera view during event (left, right, rear, center)
      - `created_at` (timestamptz) - Record creation timestamp

  2. Security
    - Enable RLS on `system_logs` table
    - Add policy for public access to allow logging without authentication
    - This is appropriate for a demo/prototype automotive system

  3. Indexes
    - Index on timestamp for efficient time-based queries
    - Index on event_type for filtering by event category

  4. Purpose
    - Tracks all system events, indicator changes, camera switches, AI detections, and warnings
    - Provides audit trail for debugging and analysis
    - Supports data visualization and system performance monitoring
*/

CREATE TABLE IF NOT EXISTS system_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp timestamptz NOT NULL DEFAULT now(),
  event_type text NOT NULL,
  details text NOT NULL,
  camera_view text,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE system_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public insert for system logging"
  ON system_logs
  FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY "Allow public read for system logs"
  ON system_logs
  FOR SELECT
  TO anon
  USING (true);

CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp 
  ON system_logs(timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_system_logs_event_type 
  ON system_logs(event_type);

CREATE INDEX IF NOT EXISTS idx_system_logs_camera_view 
  ON system_logs(camera_view) 
  WHERE camera_view IS NOT NULL;
