void dis_point_line(float _lp1[], float _lp2[], float _rp[]) {
  float slope = (_lp1[1] - _lp2[1]) / (_lp1[0] - _lp2[0]);
  // Equation line is form: Ax + By + C = 0
  float A = -slope;
  float B = 1;
  float C = (slope * _lp1[0]) - _lp1[1];
  float dis = ((A * _rp[0]) + (B * _rp[1]) + C) / sqrtf(sq(A) + sq(B)) ;
//  debug.println("A: " + String(A) + ",B: " + String(B) + ",C: " + String(C));
//  debug.println("distance: " + String(dis));
}
