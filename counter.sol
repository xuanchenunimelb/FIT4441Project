// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Counter {
  mapping (string => uint32) private store;

  function get(string memory key)
  public view
  returns (uint32 value)
  {
    return store[key];
  }

  function set(string memory key, uint32 value)
  public
  {
    store[key] = value;
  }
}