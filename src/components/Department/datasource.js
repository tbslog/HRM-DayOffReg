export const summaryData = [
  {
    DeptID: 1,
    name: "LOG 1",
    key: 1,
    DeptLevel: 60,
    note: "TBS LOGISTICS",
    children: [
      {
        DeptID: 11,
        name: "IT",
        key: 11,
        DeptLevel: 42,
        note: "IT Bình Dương",
        children: [
          {
            DeptID: 111,
            key: 111,
            name: "IT Main",
            DeptLevel: 42,
            note: "Phần Cứng",
          },
          {
            DeptID: 112,
            key: 112,
            name: "IT Dev",
            DeptLevel: 42,
            note: "Phần Mềm",
          },
        ],
      },

      {
        DeptID: 12,
        key: 12,
        name: "TBS LAND",
        DeptLevel: 30,
        note: "TBS LAND",
        children: [
          {
            DeptID: 121,
            key: 121,
            name: "TBS Bình Dương LAND",
            DeptLevel: 16,
            note: "Bình Dương",
          },
        ],
      },
      {
        DeptID: 13,
        key: 13,
        name: "Jim Green sr.",
        DeptLevel: 72,
        note: "London No. 1 Lake Park",
        children: [
          {
            DeptID: 131,
            key: 131,
            name: "Jim Green",
            DeptLevel: 42,
            note: "London No. 2 Lake Park",
            children: [
              {
                DeptID: 1311,
                key: 1311,
                name: "Jim Green jr.",
                DeptLevel: 25,
                note: "London No. 3 Lake Park",
              },
              {
                DeptID: 1312,
                key: 1312,
                name: "Jimmy Green sr.",
                DeptLevel: 18,
                note: "London No. 4 Lake Park",
              },
            ],
          },
        ],
      },
    ],
  },
  {
    DeptID: 2,
    name: "Joe Black",
    DeptLevel: 32,
    note: "Sydney No. 1 Lake Park",
  },
];
