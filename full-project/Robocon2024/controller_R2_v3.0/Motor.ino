void trans(byte data[], int datasize, int datareply, int mid) {
  byte reply[datareply];
  bool success = false;
  int count = 0;
  while (success == false) {
    serialM.write(data, datasize);
    delay(5);
    if (serialM.available() > 0) {
      serialM.readBytes(reply, datareply);
    }

    //    for (int i = 0; i < datareply; i++) {
    //      debug.print(reply[i], HEX);
    //      debug.print(" ");
    //    }
    //    debug.println();

    byte checksum = reply[0] + reply[1] + reply[2] + reply[3];
    if (reply[0] == 0x3e && reply[1] == 0xa2 && reply[2] == mid && reply[3] == 0x07 && reply[4] == checksum) {
      success = true;
    } else {
      success = false;
      count++;
      //      debug.println(count);
    }
    if (count > 10) {
      break;
    }
  }
}

void run_speed(int mid, long velo) {
  byte speed[10] = { 0x3e, 0xa2, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
  long ratio = velo * 100 * 10;
  speed[9] = 0;
  speed[2] = mid;
  speed[4] = speed[0] + speed[1] + speed[2] + speed[3];
  for (int i = 5; i < 9; i++) {
    speed[i] = ratio >> (8 * (i - 5));
    speed[9] += speed[i];
  }

  trans(speed, 10, 13, mid);
}

void initcam(double _w) {
  float tim = (360 / _w) + 0.08;
  _w = radians(_w);
  w1 = degrees(-(_w * (lx + ly) / r));
  w2 = degrees((_w * (lx + ly) / r));
  w3 = degrees(-(_w * (lx + ly) / r));
  w4 = degrees((_w * (lx + ly) / r));
  run_speed(1, w1);
  run_speed(2, -w2);
  run_speed(3, w3);
  run_speed(4, -w4);
  delay(tim * 1000);
  run_speed(1, 0);
  run_speed(2, 0);
  run_speed(3, 0);
  run_speed(4, 0);
}

void motorMotion(double _vx, double _vy, double _w, double _dis, double _ang, double _ta) {
  _dis += offset;
  _ang += offsetang;
  _w = radians(_w);
  _ang = radians(_ang);
  double _dxa, _dya;
  double _t = 0;
  double _ax = (_vx / _ta);
  double _ay = (_vy / _ta);
  double _aw = (_w / _ta);

  if (_vx != 0 || _vy != 0) {
    if (_ax != 0) {
      _dxa = sq(_vx) / (2 * _ax);  // distance acceleration for 100ms
    } else {
      _dxa = 0;
    }
    if (_ay != 0) {
      _dya = sq(_vy) / (2 * _ay);
    } else {
      _dya = 0;
    }
    double _da = sqrt(sq(_dxa) + sq(_dya));
    double _d = _dis - (2 * _da);
    double _v = sqrt(sq(_vx) + sq(_vy));
    _t = abs(_d / _v);
  } else {
    double _anga = abs(sq(_w) / (2 * _aw));
    double _angl = _ang - (2 * _anga);
    _t = abs(_angl / _w);
  }
  long countTa = 0;
  long countTt = 0;
  double _vxx = 0;
  double _vyy = 0;
  double _ww = 0;

  double tmp = 0;
  while (countTa <= _ta * 1000) {
    long t1 = millis();
    _vxx += _ax * tmp / 1000;
    _vyy += _ay * tmp / 1000;
    _ww += _aw * tmp / 1000;
    w1 = degrees(((_vxx - _vyy) - (_ww * (lx + ly))) / r);
    w2 = degrees(((_vxx + _vyy) + (_ww * (lx + ly))) / r);
    w3 = degrees(((_vxx + _vyy) - (_ww * (lx + ly))) / r);
    w4 = degrees(((_vxx - _vyy) + (_ww * (lx + ly))) / r);
    run_speed(1, w1);
    run_speed(2, -w2);
    run_speed(3, w3);
    run_speed(4, -w4);
    //    debug.println("w1: " + String(w1) + ",w2: " + String(w2) + ",w3: " + String(w3) + ",w4: " + String(w4));
    long t2 = millis();
    countTa += (t2 - t1);
    tmp = (t2 - t1);
    //    delay(100 - (t2 - t1));

    //    _vxx += _ax * tmp / 1000;
    //    _vyy += _ay * tmp / 1000;
    //    _ww += _aw * tmp / 1000;
    //    pid(_vxx, _vyy, _ww);
    //    //    debug.println("w1: " + String(w1) + ",w2: " + String(w2) + ",w3: " + String(w3) + ",w4: " + String(w4));
    //    long t2 = millis();
    //    countTa += (t2 - t1);
    //    tmp = t2 - t1;
  }

  delay(_t * 1000);

  //  pidx = _vxx;
  //  pidy = _vyy;
  //  pidw = _ww;
  //  while (countTt <= _t * 1000) {
  //    long t1 = millis();
  //    pid(_vxx, _vyy, _ww);
  //    //    debug.println("w1: " + String(w1) + ",w2: " + String(w2) + ",w3: " + String(w3) + ",w4: " + String(w4));
  //    long t2 = millis();
  //    countTt += (t2 - t1);
  //  }

  countTa = 0;
  tmp = 0;

  while (countTa <= _ta * 1000) {
    long t1 = millis();
    _vxx -= _ax * tmp / 1000;
    _vyy -= _ay * tmp / 1000;
    _ww -= _aw * tmp / 1000;

    w1 = degrees(((_vxx - _vyy) - (_ww * (lx + ly))) / r);
    w2 = degrees(((_vxx + _vyy) + (_ww * (lx + ly))) / r);
    w3 = degrees(((_vxx + _vyy) - (_ww * (lx + ly))) / r);
    w4 = degrees(((_vxx - _vyy) + (_ww * (lx + ly))) / r);
    run_speed(1, w1);
    run_speed(2, -w2);
    run_speed(3, w3);
    run_speed(4, -w4);
    //    debug.println("w1: " + String(w1) + ",w2: " + String(w2) + ",w3: " + String(w3) + ",w4: " + String(w4));
    long t2 = millis();
    countTa += (t2 - t1);
    tmp = (t2 - t1);
    //    delay(100 - (t2 - t1));

    //    _vxx -= (_ax * tmp) / 1000 ;
    //    _vyy -= (_ay * tmp) / 1000;
    //    _ww -= (_aw * tmp) / 1000;
    //
    //    Serial.println(_vxx);
    //    pid(_vxx, _vyy, _ww);
    //
    //    //    debug.println("w1: " + String(w1) + ",w2: " + String(w2) + ",w3: " + String(w3) + ",w4: " + String(w4));
    //    long t2 = millis();
    //
    //    countTa += (t2 - t1);
    //    tmp = t2 - t1;
    //    //    delay(100 - (t2 - t1));
  }

  pidx = 0;
  pidy = 0;
  pidw = 0;

  run_speed(1, 0);
  run_speed(2, 0);
  run_speed(3, 0);
  run_speed(4, 0);
}

void motion_ball(double ang, double _w) {
  float tim = (ang / _w);
  _w = radians(_w);
  w1 = degrees(-(_w * (lx + ly) / r));
  w2 = degrees((_w * (lx + ly) / r));
  w3 = degrees(-(_w * (lx + ly) / r));
  w4 = degrees((_w * (lx + ly) / r));
  run_speed(1, w1);
  run_speed(2, -w2);
  run_speed(3, w3);
  run_speed(4, -w4);
  delay(tim * 1000);
  //  run_speed(1, 0);
  //  run_speed(2, 0);
  //  run_speed(3, 0);
  //  run_speed(4, 0);
}

void ball_detect() {

  double ang_speed = 30;
  double errorpixx, spixx, ppixx, ipixx, dpixx, pre_errorpixx, pidpixx;

  spixx = 300;
  pidpixx = 0;

  while (true) {
    //    debug.print("read");
    //    int countsr = 0;
    //    while (debug.available() == 0) {
    //      delay(1);
    //      countsr++;
    //      if (countsr >= 1000) {
    //        break;
    //      }
    //    }
    //    if (debug.available() > 0) {
    //      debug.flush();
    //      String cmd = debug.readString();
    //      deserialJson(cmd);
    //    }
    
//    if (Start == 0) {
//      run_speed(1, 0);
//      run_speed(2, 0);
//      run_speed(3, 0);
//      run_speed(4, 0);
//      break;
//    }
    if (detect == 1) {
      errorpixx = spixx - pixx;
      ppixx = errorpixx * kpx;
      ipixx = kix * (ipixx + errorpixx);
      dpixx = kdx * (errorpixx - pre_errorpixx);
      pre_errorpixx = errorpixx;
      double correctpixx = ppixx + ipixx + dpixx;
      pidpixx = correctpixx;
      pidpixx = _min(90, pidpixx);
      pidpixx = _max(-90, pidpixx);

      pidpixx = radians(pidpixx);
      w1 = degrees(-(pidpixx * (lx + ly) / r));
      w2 = degrees((pidpixx * (lx + ly) / r));
      w3 = degrees(-(pidpixx * (lx + ly) / r));
      w4 = degrees((pidpixx * (lx + ly) / r));
      run_speed(1, w1);
      run_speed(2, -w2);
      run_speed(3, w3);
      run_speed(4, -w4);
    } else {
      pidpixx = 0;
      ppixx = 0;
      ipixx = 0;
      dpixx = 0;
      pre_errorpixx = 0;
      run_speed(1, 0);
      run_speed(2, 0);
      run_speed(3, 0);
      run_speed(4, 0);
    }

    if (errorpixx > -10 && errorpixx < 10) {
      break;
    }
  }

  //  motorMotion(500, 0, 0, Dis, 0, 1);
}

void pid(double spx, double spy, double spw) {
  debug.print("read");
  int countsr = 0;
  while (debug.available() == 0) {
    delay(1);
    countsr++;
    if (countsr >= 1000) {
      break;
    }
  }
  if (debug.available() > 0) {
    debug.flush();
    String cmd = debug.readString();
    //    debug.println(cmd);
    deserialJson(cmd);
  }

  errorx = spx - (vx * 1000);
  px = errorx * kpx;
  ix = kix * (ix + errorx);
  dx = kdx * (errorx - pre_errorx);
  pre_errorx = errorx;
  double correctx = px + ix + dx;
  pidx = pidx + correctx;
  pidx = _min(maxsp, pidx);
  pidx = _max(minsp, pidx);

  errory = spy - (vy * 1000);
  py = errory * kpy;
  iy = kiy * (iy + errory);
  dy = kdy * (errory - pre_errory);
  pre_errory = errory;
  double correcty = py + iy + dy;
  pidy = pidy + correcty;
  pidy = _min(maxsp, pidy);
  pidy = _max(minsp, pidy);

  errorw = spw - w;
  pw = errorw * kpw;
  iw = kiw * (iw + errorw);
  dw = kdw * (errorw - pre_errorw);
  pre_errorw = errorw;
  double correctw = pw + iw + dw;
  pidw = pidw + correctw;
  pidw = _min(maxspw, pidw);
  pidw = _max(minspw, pidw);

  w1 = degrees(((pidx - pidy) - (pidw * (lx + ly))) / r);
  w2 = degrees(((pidx + pidy) + (pidw * (lx + ly))) / r);
  w3 = degrees(((pidx + pidy) - (pidw * (lx + ly))) / r);
  w4 = degrees(((pidx - pidy) + (pidw * (lx + ly))) / r);
  run_speed(1, w1);
  run_speed(2, -w2);
  run_speed(3, w3);
  run_speed(4, -w4);
}
