{
	'cflags':
	[
		'-fstrict-aliasing',
		'-fvisibility=hidden',
	],
	
	'cflags_c':
	[
		'-std=gnu99',
		'-Wstrict-prototypes',
	],
	
	'cflags_cc':
	[
		'-std=c++03',
		'-fno-exceptions',
		'-fno-rtti',
	],

	'target_conditions':
	[
		[
			'silence_warnings == 0',
			{
				'cflags':
				[
					'-Wall',
					'-Wextra',
					'-Wno-unused-parameter',	# Just contributes build noise
				],
				
				'cflags_c':
				[
					'-Werror=declaration-after-statement',	# Ensure compliance with C89
				],
			},
			{
				'cflags':
				[
					'-w',						# Disable warnings
					'-fpermissive',				# Be more lax with old code
					'-Wno-return-type',
				],
			},
		],
		[
			'supports_lto != 0',
			{
				'ldflags':
				[
					'-fuse-ld=gold',
				],

				'arflags':
				[
					'--plugin', '<!(echo $(dirname <(ar))/../lib/LLVMgold.so)',
				],
			},
			{
				'ldflags':
				[
					'-fuse-ld=bfd',
				],
			},
		],
	],
	
	'configurations':
	{
		'Debug':
		{
			'cflags':
			[
				'-O0',
				'-g3',
			],
			
			'defines':
			[
				'_DEBUG',
			],
		},
		
		'Release':
		{
			'cflags':
			[
				'-O3',
				'-g3',
			],

			'conditions':
			[
				[
					'supports_lto != 0',
					{
						'cflags':
						[
							'-flto',
							'-ffunction-sections',
						],

						'ldflags':
						[
							'-Wl,--icf=all',
							'>@(_cflags)',
							'>@(_cflags_cc)',
							
						],
					},
				],
			],
			
			'defines':
			[
				'_RELEASE',
				'NDEBUG',
			],
		},
		
		'Fast':
		{
			'cflags':
			[
				'-O0',
				'-g0',
			],
			
			'defines':
			[
				'_RELEASE',
				'NDEBUG',
			],
		},
	},
	
	'defines':
	[
		'TARGET_PLATFORM_MOBILE',
		'TARGET_SUBPLATFORM_ANDROID',
		'ANDROID',
		'_MOBILE',
		'ANDROID_NDK',
	],
}
